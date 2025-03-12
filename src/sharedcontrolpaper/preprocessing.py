import os
import pandas as pd
import glob
import re
from pathlib import Path
import logging
import numpy as np
from force_sensitive_stopping_task_utils import get_subject_label

def change_columns():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two directories
    parent_directory = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))

    #Simple Stop Data
    simple_stop_data_path = os.path.join(parent_directory, 'experiments', 'simpleStop', 'data')
    simple_stop_files = glob.glob(os.path.join(simple_stop_data_path, '*.csv'))  #Get all CSV files


    for file in simple_stop_files:
        subject_label = get_subject_label(file)
        df = pd.read_csv(file)
        df = df[['Block', 'Phase', 'trialType', 'goStim', 'ssd', 'goResp_test.keys', 'correctResponse',
                 'goResp_test.rt', 'goResp.keys', 'goResp.rt']]

        df.rename(columns={'goResp_test.keys': 'response', 'goResp_test.rt': 'rt',
                           'goResp.keys': 'response', 'goResp.rt': 'rt'}, inplace=True)

        def same_merge(x):
            return ','.join(x[x.notnull()].astype(str))

        df.dropna(how='all', inplace=True)
        df = df.groupby(level=0, axis=1).apply(lambda x: x.apply(same_merge, axis=1))

        output_path = os.path.join(parent_directory, 'data', 'experiment', 'final', f'sub-{subject_label}', 'simple_stop',
                                   f'{subject_label}_simple_stop.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Create directories if they don't exist
        df.to_csv(output_path, index=False)


    #Force Sensitive Stopping Task Data
    shared_control_data_path = os.path.join(parent_directory, 'experiments', 'forceSensitiveStoppingTask')
    shared_control_files = glob.glob(os.path.join(shared_control_data_path, '*.csv'))


    for file in shared_control_files:
        subject_label = get_subject_label(file)
        df = pd.read_csv(file, index_col=0)
        df = df.drop(['extraInfo', 'participant', 'session'], axis=0)
        df = df.drop(columns=['SSD_mean', 'SSD_std', 'n', 'condition_order_mean', 'condition_order_std', 'order',
                              'phase_raw'], axis=1)
        df.reset_index(inplace=True)
        df.rename(columns={
            'SSD_raw': 'SSD',
            'block_raw': 'block',
            'distances_raw': 'distances',
            'pressures_raw': 'pressures',
            'time_stamps_raw': 'time_stamps'
        }, inplace=True)

        df['block'] = df['block'].str.strip().str.replace(r"['\"]", '', regex=True)

        if df['condition_order_raw'].iloc[0] == 1:
            df.loc[(df['block'] == 'block 1') & (df['condition'] == 'stop'), 'condition'] = 'Non-AI'
            df.loc[(df['block'].isin(['block 2', 'practice'])) & (df['condition'] == 'stop'), 'condition'] = 'AI-failed'
            df.loc[df['condition'] == 'ai', 'condition'] = 'AI-assisted'

        else:
            df.loc[(df['block'] == 'block 2') & (df['condition'] == 'stop'), 'condition'] = 'Non-AI'
            df.loc[(df['block'].isin(['block 1', 'practice'])) & (df['condition'] == 'stop'), 'condition'] = 'AI-failed'
            df.loc[df['condition'] == 'ai', 'condition'] = 'AI-assisted'

        df = df.drop(columns=['condition_order_raw'], axis=1)

        output_path = os.path.join(parent_directory, 'data', 'experiment', 'final', f'sub-{subject_label}',
                                   'force_sensitive_stopping_task',
                                   f'{subject_label}_force_sensitive_stopping_task.csv')
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Create directories if they don't exist
        df.to_csv(output_path, index=False)

def extract_numeric_values(values):
    return [float(x) for x in values.replace("'", "").split(' ')]

def extract_data(row):
    # Extract arrays from the row
    distances_array = extract_numeric_values(row['distances'])
    pressures_array = extract_numeric_values(row['pressures']) 
    time_stamps_array = extract_numeric_values(row['time_stamps'])

    # Verify all arrays have the same length
    array_lengths = {
        'distances': len(distances_array),
        'pressures': len(pressures_array),
        'time_stamps': len(time_stamps_array)
    }
    
    if len(set(array_lengths.values())) != 1:
        msg = "All arrays must have the same length: "
        msg += ", ".join(f"{name}={length}" for name, length in array_lengths.items())
        raise ValueError(msg)

    return distances_array, pressures_array, time_stamps_array

def check_amount_of_trials(df_tidy, expected_amount_of_trials=220):
    end_trial_number = df_tidy['sub_trial'].str.split('_').str[1].astype(int).max()
    if end_trial_number != expected_amount_of_trials:
        msg = f"Amount of trials is not {expected_amount_of_trials}, found {end_trial_number}"
        raise ValueError(msg)
    
def add_ring_positions(df, ring_positions_raw):
    """Adds ring positions to distances, handling zero pressures."""
    df_new = df.copy()
    current_subtrial = None
    ring_position_index = 0
    distances = []
    for index, row in df.iterrows():
        sub_trial = row['sub_trial']
        relative_distances = row['relative_distances']
        ssd = row['SSD']

        if sub_trial != current_subtrial:
            ring_position_index = 0
            total_distance = row['relative_distances'] + -14.905 #This is the distance of the ring as soon as it starts moving
            current_subtrial = sub_trial

        if 0 <= ring_position_index < len(ring_positions_raw):
            if row['time_stamps'] >= ssd and row['condition'] == 'AI-assisted':
                total_distance = total_distance
            elif row['pressures'] != 0:
                ring_position = ring_positions_raw[ring_position_index]
                total_distance = relative_distances + ring_position
            elif row['pressures'] == 0:
                total_distance = total_distance
            distances.append(total_distance) 
        else:
            distances.append(total_distance) 
        ring_position_index += 1

    df_new['distances'] = distances
    return df_new

def process_distance_data(df, ring_positions_raw):
    """Processes a single DataFrame, adds ring positions, and returns the modified DataFrame."""
    df = df.rename(columns={'distances': 'relative_distances'})
    df = add_ring_positions(df, ring_positions_raw)
    cols = df.columns.tolist()
    cols.remove('distances')
    cols.insert(cols.index('relative_distances') + 1, 'distances')
    df = df[cols]
    return df

def main():
    logging.basicConfig(level=logging.INFO)
    data_dir = Path("data", "experiment", "final")
    outdir = data_dir
    outdir.mkdir(parents=True, exist_ok=True)
    subjects = sorted(data_dir.glob("sub-s*")) # Change this if you only want to run the script on some subjects
    for subject in subjects:
        logging.info(f"Processing subject {subject}")
        sub_id = subject.name.replace("sub-", "")
        # input and output paths are now the same
        filepath = subject / "force_sensitive_stopping_task" / f'{sub_id}_force_sensitive_stopping_task.csv'

        assert filepath.exists(), f"Force sensitive task not found for {subject}"
        df = pd.read_csv(filepath)

        df_tidy = pd.DataFrame()
        for index, row in df.iterrows():
            trial_number = index + 1
            condition = row['condition']
            SSD = row['SSD']
            block = row['block']
            distances, pressures, time_stamps = extract_data(row)
            
            rows = []
            for d in zip(distances, pressures, time_stamps):
                row = {
                    'condition': condition,
                    'SSD': SSD,
                    'block': block,
                    'distances': d[0],
                    'pressures': d[1],
                    'time_stamps': d[2], 
                    'sub_trial': f'{sub_id}_{trial_number}'
                }
                rows.append(row)
            
            df_tidy = pd.concat([df_tidy, pd.DataFrame(rows)], ignore_index=True)

        check_amount_of_trials(df_tidy)
        ring_positions_raw = np.arange(-14.905, 15.095, 0.095).tolist()
        df_tidy = process_distance_data(df_tidy, ring_positions_raw)
        outpath = filepath
        df_tidy.to_csv(outpath, index=False)

    return


if __name__ == "__main__":
    change_columns()  # Run the first part of the preprocessing
    main()             # Run the second part (tidy data creation)