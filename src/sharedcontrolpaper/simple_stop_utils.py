import pandas as pd
import numpy as np

# Add columns for stop acc, go acc, and stop failure acc
def preprocess_stop_data(df):
    df['ssd'] = df['ssd'] * 1000
    df['goResp_test.rt'] = df['goResp_test.rt'] * 1000

    df.loc[:, 'stop_acc'] = np.where(df['trialType'] == 'stop', 
                                 np.where(df['response'].isnull(), 1, 0),  
                                 np.nan)

    df.loc[:, 'go_acc'] = np.where(df['trialType'] == 'go', 
                                   np.where(df['response'] == df['correctResponse'], 1, 0), 
                                   np.nan)

    df.loc[:, 'stop_failure_acc'] = np.where(
        (df['trialType'] == 'stop') & (df['rt'].notna()),
        np.where(df['response'] == df['correctResponse'], 1, 0),
        np.nan)
    
    return df

def compute_SSRT(df, without_short_ssd_trials = False, max_go_rt = 2):
    """
    Compute Stop Signal Reaction Time (SSRT) for the simple stop task.

    Parameters:
    - df: DataFrame containing trial data.
    - without_short_ssd_trials: boolean to compute SSRT without short SSD trials when set to True.
    - max_go_rt: Maximum allowed reaction time for go trials to replace missing values.

    Returns:
    - SSRT: The computed Stop Signal Reaction Time.
    """
    if without_short_ssd_trials:
        df = df[df['ssd'] >= 200] 

    avg_SSD = None
    
    df = df.query('Phase == "test"')
    
    go_trials = df.loc[df.trialType == 'go']
    stop_df = df.loc[df.trialType == 'stop']

    go_replacement_df = go_trials.where(~go_trials['rt'].isna(), max_go_rt)
    sorted_go = go_replacement_df.rt.sort_values(ascending = True, ignore_index=True)
    stop_failure = stop_df.loc[stop_df['rt'].notna()]

    if len(stop_df) > 0 and len(stop_failure) > 0:
        p_respond = len(stop_failure)/len(stop_df) # proportion of stop trials where there was a response
        avg_SSD = stop_df.ssd.mean()
    else:
        SSRT = None
    nth_index = int(np.rint(p_respond*len(sorted_go))) - 1 

    if nth_index < 0:
        nth_RT = sorted_go[0]
    elif nth_index >= len(sorted_go):
        nth_RT = sorted_go[-1]
    else:
        nth_RT = sorted_go[nth_index]
    
    if avg_SSD:
        SSRT = nth_RT - avg_SSD
    else:
        SSRT = None
    return SSRT

def analyze_violations(df):
    violations_data = []

    for i in range(len(df) - 1):  # Go until the second to last trial
        # Check for a Go trial followed by a Stop trial with a violation
        if (df.iloc[i]['trialType'] == 'go' and
            df.iloc[i + 1]['trialType'] == 'stop' and
            pd.notna(df.iloc[i + 1]['rt'])):
            
            go_rt = df.iloc[i]['rt']         # RT of Go trial
            stop_rt = df.iloc[i + 1]['rt']  # RT of Stop trial
            
            if pd.notna(go_rt) and pd.notna(stop_rt):  # Ensure RTs are valid
                difference = stop_rt - go_rt  # Calculate the difference
                ssd = df.iloc[i + 1]['ssd']    # SSD for the Stop trial
                violations_data.append({'difference': difference, 'ssd': ssd})

    return pd.DataFrame(violations_data)