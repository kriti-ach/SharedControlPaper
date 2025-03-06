import numpy as np
import re
from matplotlib.ticker import MultipleLocator
import pandas as pd
from scipy import stats
from sharedcontrolpaper.simple_stop_utils import SECONDS_TO_MILLISECONDS

RING_RADIUS_THRESHOLD = 1.2 # Distance that needs to be cleared for the dot to be outside the ring
MINIMUM_SSRT = 0.175 # The minimum delay after the stop signal before checking for inhibition, in seconds
NEXT_N_POINTS = 4 # Check if the next N of these points follow the criteria to categorize SSRT
MAX_PRESSURE = 1 # Pressure when the subject is fully pressing the spacebar
MIN_PRESSURE = 0 # Pressure when the subject is not pressing the spacebar
THRESHOLD_REDUCTION = 0.30 # Check for this much reduction in pressure to start checking for SSRT
INTERVAL_DURATION = 0.1 # Duration of a time interval, in seconds

def get_subject_label(file):
    """Extract the subject label from a given file path."""
    
    match = re.search(r'/sub-(s\d{3})/', file)
    
    if match:
        subject_label = match.group(1)
        return subject_label
    else:
        return None
    
def aggregate_trial_data(df):
    """Aggregates trial data, handling AI-assisted and Non-AI conditions."""

    agg_cols = {
        'distances': list,
        'relative_distances': list,
        'pressures': list,
        'time_stamps': list,
        'condition': 'first',
        'SSD': 'first',
        'block': 'first',
    }
    return df.groupby('sub_trial').agg(agg_cols).reset_index()

def calculate_interval_average(group):
    """Calculates the average pressure for a given time interval."""
    return np.mean(group['pressures'])


def calculate_intervals(time_stamps, pressures, stop_onset, interval_duration=INTERVAL_DURATION):
    """Calculates average pressures at specified intervals until stop onset using Pandas."""

    df = pd.DataFrame({'time_stamps': time_stamps, 'pressures': pressures})

    #Efficiently filter the dataframe to include only data points before stop_onset
    df_before_stop = df[df['time_stamps'] < stop_onset]

    #Create interval labels
    df_before_stop = df_before_stop.copy()
    df_before_stop.loc[:, 'interval'] = (df_before_stop['time_stamps'] // interval_duration).astype(int)

    # Group data by interval and calculate average pressure for each
    pressures_at_intervals = df_before_stop.groupby('interval').apply(calculate_interval_average)

    return pressures_at_intervals.tolist()

def is_monotonic_decrease(series):
    """Checks if a Pandas Series exhibits a monotonic decrease."""
    return series.is_monotonic_decreasing

def check_pressure_drop(series, threshold):
    """Checks if a pressure drop below a threshold occurs within a series."""
    return (series <= threshold).any()


def find_ssrt(time_stamps, pressures, start_index):
    """
    Finds the stop-signal reaction time (SSRT) using Pandas.

    Args:
        time_stamps: Array-like of timestamps.
        pressures: Array-like of pressure measurements.
        start_index: Index to start searching for SSRT.

    Returns:
        A tuple containing the SSRT (in time units) and its index, or (np.nan, None) if not found.
    """
    df = pd.DataFrame({'time_stamps': time_stamps, 'pressures': pressures})

    for i in range(start_index, len(pressures)):
        current_pressure = pressures[i]
        target_pressure = current_pressure * (1 - THRESHOLD_REDUCTION)

        # Check if we have enough points for the next N
        if i + NEXT_N_POINTS <= len(pressures):
            next_pressures = df['pressures'][i + 1:i + 1 + NEXT_N_POINTS]
            #Handle case where pressure is max:
            if next_pressures.eq(MAX_PRESSURE).any():
                continue
            
            if is_monotonic_decrease(next_pressures) and check_pressure_drop(next_pressures, target_pressure):
                return df['time_stamps'][i], i

    return np.nan, None

def find_stop_onset_idx(time_stamps, stop_onset):
    """Finds the index of the first timestamp greater than or equal to stop_onset."""
    return next((i for i, t in enumerate(time_stamps) if t >= stop_onset), None)

def find_min_ssrt(time_stamps, stop_onset):
    """Finds the index of the first timestamp greater than or equal to stop_onset + MINIMUM_SSRT."""
    minimum_ssrt_for_trial = stop_onset + MINIMUM_SSRT
    min_ssrt_for_trial_index = next((i for i, t in enumerate(time_stamps) if t >= minimum_ssrt_for_trial), None)
    return minimum_ssrt_for_trial, min_ssrt_for_trial_index

def find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures):
    """Finds the timestamp and index when pressure first reaches zero after ssrt_index."""
    pressure_reached_zero = np.nan
    pressure_reached_zero_idx = None
    if ssrt_index is not None:
        stop_moment_indices = [i for i in range(ssrt_index, len(pressures)) if pressures[i] == 0]
        if stop_moment_indices:
            pressure_reached_zero = time_stamps[stop_moment_indices[0]]
            pressure_reached_zero_idx = stop_moment_indices[0]
    return pressure_reached_zero, pressure_reached_zero_idx

def find_duration_of_inhibition(ssrt, pressure_reached_zero):
    """Calculates the duration between ssrt and the moment pressure reaches zero."""
    duration_of_inhibition = np.nan
    if not np.isnan(ssrt) and pressure_reached_zero is not None:
        duration_of_inhibition = pressure_reached_zero - ssrt
    return duration_of_inhibition

def find_ssrt_relative_to_stop_onset(ssrt, stop_onset):
    """Calculates ssrt relative to stop_onset."""
    if stop_onset is not None and not np.isnan(ssrt):
        ssrt = ssrt - stop_onset
    return ssrt

def calculate_proportions(series, threshold):
    """Calculates proportions of relative_distances before, inside, and after a threshold."""
    inside = (series.abs() <= threshold).sum()
    after = (series > threshold).sum()
    total = len(series)
    return inside / total if total else np.nan, after / total if total else np.nan


def calculate_go_task_metrics(relative_distances, stop_onset_idx, ring_radius_threshold=RING_RADIUS_THRESHOLD):
    """Calculates go task accuracy metrics using Pandas."""

    df = pd.Series(relative_distances) #Pandas Series for efficient operations

    results = {}

    if stop_onset_idx is not None:
        # Before stop signal
        before_stop = df[:stop_onset_idx]
        before_accuracy, before_prop_after = calculate_proportions(before_stop, ring_radius_threshold)
        results['go_task_accuracy_before_stop_onset'] = before_accuracy
        results['ball_after_ring_proportion_before_stop_onset'] = before_prop_after

        # At stop signal
        results['go_task_accuracy_at_stop_onset'] = 1 if abs(df[stop_onset_idx]) <= ring_radius_threshold else 0

        # After stop signal
        after_stop = df[stop_onset_idx + 1:]
        after_accuracy, after_prop_after = calculate_proportions(after_stop, ring_radius_threshold)
        results['go_task_accuracy_after_stop_onset'] = after_accuracy
        
    else:
        results['go_task_accuracy_before_stop_onset'] = np.nan
        results['ball_after_ring_proportion_before_stop_onset'] = np.nan
        results['go_task_accuracy_at_stop_onset'] = np.nan
        results['go_task_accuracy_after_stop_onset'] = np.nan

    return results

def find_first_non_zero_pressure_timestamp(pressures, time_stamps):
    """Finds the timestamp of the first occurrence of a pressure exceeding the minimum pressure."""
    first_non_zero_pressure_timestamp = np.nan
    for i, pressure in enumerate(pressures):
        if pressure > MIN_PRESSURE:
            first_non_zero_pressure_timestamp = time_stamps[i]
            break
    return first_non_zero_pressure_timestamp

def find_first_full_pressure_timestamp(pressures, time_stamps):
    """Finds the timestamp of the first occurrence of a pressure at the maximum pressure."""
    first_full_pressure_timestamp = np.nan
    for i, pressure in enumerate(pressures):
        if pressure == MAX_PRESSURE:
            first_full_pressure_timestamp = time_stamps[i] 
            break
    return first_full_pressure_timestamp

def find_stops_before_stop_onset(pressures, stop_onset_idx):
    """Calculates the proportion of times pressure drops to zero before the stop signal."""
    if stop_onset_idx is None or stop_onset_idx <= 0:
        return np.nan

    relevant_pressures = pressures[:stop_onset_idx]
    num_zero_pressures = np.size(relevant_pressures) - np.count_nonzero(relevant_pressures)
    proportion_zero = num_zero_pressures / len(relevant_pressures) if len(relevant_pressures)>0 else np.nan


    return proportion_zero

def process_trial_data(data, block):
    """Process trial data for a specific block, calculating metrics including SSRT,
    moment of inhibition, and pressure measures."""
    trial_results = {}
    ssrt_list = []

    for idx, row in data.iterrows():
        trial_number = idx
        stop_onset = row['SSD']

        if stop_onset is None:
            raise ValueError(f"Stop onset (SSD) is missing for trial {trial_number}.")
        
        time_stamps = row['time_stamps']
        pressures = row['pressures']
        condition = row['condition']
        distances = row['distances']
        relative_distances = row['relative_distances']

        # Find the index of stop onset
        stop_onset_idx = find_stop_onset_idx(time_stamps, stop_onset)

        # Calculate the minimum time to start checking for inhibition and its index for the given trial
        min_ssrt_for_trial, min_ssrt_for_trial_index = find_min_ssrt(time_stamps, stop_onset)
        
        # Calculate the SSRT and the index of SSRT
        ssrt, ssrt_index = find_ssrt(time_stamps, pressures, min_ssrt_for_trial_index)

        # Calculate the SSRT without a minimum SSRT and its index
        ssrt_no_min, ssrt_no_min_index = find_ssrt(time_stamps, pressures, stop_onset_idx)

        # Find the moment the pressure on the keyboard reached 0 and its index
        pressure_reached_zero, pressure_reached_zero_idx = find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures)
                
        # Find the duration of inhibition (time between moment of inhibition and end of inhibition) 
        duration_of_inhibition = find_duration_of_inhibition(ssrt, pressure_reached_zero)
                
        # Calculate SSRT and SSRT no min relative to the stop onset
        ssrt = find_ssrt_relative_to_stop_onset(ssrt, stop_onset)
        ssrt_no_min = find_ssrt_relative_to_stop_onset(ssrt_no_min, stop_onset)
        ssrt_list.append(ssrt)

        # Calculate Go Task Accuracy metrics
        results = calculate_go_task_metrics(relative_distances, stop_onset_idx)

        # Find the pressures at time intervals until stop onset
        pressures_at_intervals_until_stop_onset = calculate_intervals(time_stamps, pressures, stop_onset)

        #Find the first timestamp with non-zero pressure
        first_non_zero_pressure_timestamp = find_first_non_zero_pressure_timestamp(pressures, time_stamps)
        first_full_pressure_timestamp = find_first_full_pressure_timestamp(pressures, time_stamps)

        proportion_stops_before_stop_onset = find_stops_before_stop_onset(pressures, stop_onset_idx)

        trial_results[trial_number] = {
            'stop_onset': stop_onset,
            'stop_moment': pressure_reached_zero,
            'stop_moment_idx': pressure_reached_zero_idx,
            'index_of_ssrt': ssrt_index,
            'duration_of_inhibition': duration_of_inhibition,
            'distances': distances,
            'pressures': pressures,
            'relative_distances': relative_distances,
            'time_stamps': time_stamps,
            'condition': condition,
            'minimum_ssrt': min_ssrt_for_trial,
            'go_task_accuracy_at_stop_onset': results['go_task_accuracy_at_stop_onset'],
            'go_task_accuracy_before_stop_onset': results['go_task_accuracy_before_stop_onset'],
            'go_task_accuracy_after_stop_onset': results['go_task_accuracy_after_stop_onset'],
            'ball_after_ring_proportion_before_stop_onset': results['ball_after_ring_proportion_before_stop_onset'],
            'pressures_at_intervals_until_stop_onset': pressures_at_intervals_until_stop_onset,
            'first_non_zero_pressure_timestamp': first_non_zero_pressure_timestamp,
            'first_full_pressure_timestamp': first_full_pressure_timestamp,
            'proportion_stops_before_stop_onset': proportion_stops_before_stop_onset,
            'ssrt': ssrt,
            'ssrt_without_minimum_ssrt': ssrt_no_min
        }
    return trial_results, ssrt_list

def collect_trial_metric(subject_data, measure, aggregate_ai=False):
    """Collects metric for a single subject, handling AI Block aggregation."""
    results = {'non_ai': [], 'ai_failed': [], 'ai_assisted': []}
    for block, block_data in subject_data.items():
        for trial, trial_data in block_data['trial_results'].items():
            metric_value = trial_data.get(measure, np.nan)
            if block == 'Non-AI':
                results['non_ai'].append(metric_value)
            elif block == 'AI':
                if aggregate_ai:
                    results['ai_failed'].append(metric_value)
                    results['ai_assisted'].append(metric_value)
                else:
                    condition = trial_data.get('condition', '')
                    if condition == 'AI-failed':
                        results['ai_failed'].append(metric_value)
                    elif condition == 'AI-assisted':
                        results['ai_assisted'].append(metric_value)
    return results


def find_sum_of_intervals(trials_list, measures_dict, max_length, subject):
    """Calculate the sum of pressures at specified intervals for trials."""
    # Pad the trials with NaN to make sure they are the same length
    trials = [np.pad(np.array(lst, dtype=float), (0, max_length - len(lst)), constant_values=np.nan) for 
                                    lst in trials_list]
    # Calculate the proportion of 1s at each interval
    counts = np.count_nonzero(~np.isnan(np.vstack(trials)), axis=0)  # Count valid entries
    measures_dict[subject] = np.nansum(np.vstack(trials) == 1, axis=0) / counts # Count number of pressures=1
    return measures_dict

def convert_dict_to_df(data_dict, time_intervals):
    """Convert a dictionary into a DataFrame, dropping NaN-only columns and adding mean or sum row."""
    df = pd.DataFrame.from_dict(data_dict, orient='index')
    df = df.dropna(axis=1, how='all')  # Remove columns that are all NaN
    df.columns = time_intervals
    df.index.name = 'subject'
    df = df.sort_values(by='subject')
    df.loc['mean across all subjects'] = df.mean()
    return df

def calculate_proportions_non_nan(results):
  """Calculates proportions of non-NaN values for each condition."""
  counts = {}
  total_counts = {}
  for condition, data_list in results.items():
    count = 0
    total_count = 0
    for val in data_list:
      if not np.isnan(val):
        count += 1
      total_count += 1

    counts[condition] = count
    total_counts[condition] = total_count

  return counts, total_counts

def convert_to_milliseconds(df):
    """Converts specified columns of a DataFrame to milliseconds."""
    for col in ['non_ai', 'ai_failed', 'ai_assisted']:
        if col in df.columns:
            df[col] *= SECONDS_TO_MILLISECONDS

def plot_trial_pressure_individual(trial_data, trial_number, ax, color):
    """Function to plot the pressure data for an individual trial. It includes vertical 
    lines marking key events such as stop onset, moment of inhibition, stop moment, 
    and post-buffer stamp."""
    pressures = trial_data['pressures']
    time_stamps = trial_data['time_stamps']
    stop_onset_time = trial_data.get('stop_onset', None)
    ssrt = trial_data.get('ssrt', None)
    
    stop_moment = trial_data.get('stop_moment', None)
    minimum_ssrt = trial_data.get('minimum_ssrt', None)

    ax.plot(time_stamps, pressures, color=color)

    if stop_onset_time is not None:
        ax.axvline(x=stop_onset_time, color='black', linestyle='dotted', linewidth=2, label='Stop Onset')
    if ssrt is not None:
        ax.axvline(x=ssrt+stop_onset_time, color='green', linestyle='dotted', linewidth=2, label='SSRT')
    if stop_moment is not None:
        ax.axvline(x=stop_moment, color='red', linestyle='dotted', linewidth=2, label='Pressure on the Keyboard Reached 0')
    if minimum_ssrt is not None:
        ax.axvline(x=minimum_ssrt, color='purple', linestyle='dotted', linewidth=2, label='Minimum SSRT')

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Raw Pressure')
    ax.legend(loc="lower left")
    ax.grid(True)

    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 3.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Major ticks at every second
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))  # Minor ticks at every 100 ms

def calculate_confidence_interval(data, confidence=0.95):
    """Calculates the confidence interval, ignoring NaN values."""
    a = np.array(data)
    valid_data = a[~np.isnan(a)]  #Filter out NaNs
    n = len(valid_data)

    if n < 2:  #Need at least 2 data points for CI calculation
        return (np.nan, np.nan)

    m, se = np.mean(valid_data), stats.sem(valid_data)
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return m - h, m + h
