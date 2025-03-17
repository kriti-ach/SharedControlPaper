import pandas as pd
import numpy as np

SECONDS_TO_MILLISECONDS = 1000
SHORT_SSD_LIMIT = 200
MAX_GO_RT = 2

def preprocess_stop_data(df): 
    """Preprocesses stop signal task data to give go accuracy, stop accuracy, and stop failure accuracy."""
    df['ssd'] = df['ssd'] * SECONDS_TO_MILLISECONDS
    df['rt'] = df['rt'] * SECONDS_TO_MILLISECONDS

    # Efficiently calculate accuracy columns using boolean indexing and assignment
    df['stop_acc'] = 0
    df.loc[(df['trialType'] == 'stop') & (df['response'].isnull()), 'stop_acc'] = 1

    df['go_acc'] = 0
    df.loc[(df['trialType'] == 'go') & (df['response'] == df['correctResponse']), 'go_acc'] = 1

    df['stop_failure_acc'] = 0
    df.loc[(df['trialType'] == 'stop') & (df['rt'].notna()) & (df['response'] == df['correctResponse']), 'stop_failure_acc'] = 1

    return df

def compute_SSRT(df, without_short_ssd_trials=False): #Added SHORT_SSD_LIMIT
    """Computes Stop Signal Reaction Time (SSRT)."""
    if without_short_ssd_trials:
        df = df[df['ssd'] >= SHORT_SSD_LIMIT]

    df = df[df['Phase'] == 'test']  # Filter for test phase

    go_trials = df[df['trialType'] == 'go']
    stop_trials = df[df['trialType'] == 'stop']

    # Handle missing RTs in go trials using fillna
    go_rts = go_trials['rt'].fillna(MAX_GO_RT)  

    # Efficiently calculate p_respond
    p_respond = stop_trials['rt'].notna().mean()  

    if len(stop_trials) > 0 and len(go_rts) > 0 :
      avg_ssd = stop_trials['ssd'].mean()
      nth_index = int(np.rint(p_respond * len(go_rts))) -1
      sorted_go_rts = go_rts.sort_values(ascending=True, ignore_index=True)

      nth_rt = sorted_go_rts.iloc[max(0, min(nth_index, len(sorted_go_rts)-1))] # Handle edge cases

      ssrt = nth_rt - avg_ssd
    else:
      ssrt = np.nan

    return ssrt


def analyze_violations(df):
    """Analyzes violations (trials where Stop Fail RT > Go RT). Note: All Go trials followed by a Stop Fail trial 
    are collected in 'violations'."""
    # Create shifted DataFrames for comparison
    df_shifted = df.shift(-1)

    # Efficiently identify violations using boolean indexing
    violations = (df['trialType'] == 'go') & (df_shifted['trialType'] == 'stop') & (df_shifted['rt'].notna())

    # Extract relevant data for violations
    result_df = pd.DataFrame({
        'difference': df_shifted.loc[violations, 'rt'].values - df.loc[violations, 'rt'].values,
        'ssd': df_shifted.loc[violations, 'ssd'].values
    })

    return result_df