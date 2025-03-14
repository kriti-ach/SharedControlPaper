import numpy as np
import re
from matplotlib.ticker import MultipleLocator
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

RING_RADIUS_THRESHOLD = 1.2 # Distance that needs to be cleared for the dot to be outside the ring
MINIMUM_SSRT = 0.175 # The minimum delay after the stop signal before checking for inhibition, in seconds
NEXT_N_POINTS = 4 # Check if the next N of these points follow the criteria to categorize SSRT
MAX_PRESSURE = 1 # Pressure when the subject is fully pressing the spacebar
MIN_PRESSURE = 0 # Pressure when the subject is not pressing the spacebar
THRESHOLD_REDUCTION = 0.30 # Check for this much reduction in pressure to start checking for SSRT
INTERVAL_DURATION = 0.1 # Duration of a time interval, in seconds. Pressures at intervals are calculated with this interval duration.
EXCLUSIONS = {"s027": ["AI", 80, 96]} # Force-sensitive stopping task trial exclusions
SECONDS_TO_MILLISECONDS = 1000 # Seconds to milliseconds conversion
SSRT_THRESHOLD_FIGURE_S2 = 600 # To plot figure S2, we excluded outliers above SSRT_THRESHOLD_FIGURE_S2.
CONFIDENCE = .95 # The confidence level for confidence intervals

QUESTION_LIST = [
    "AI is making our daily lives easier.",
    "I believe that increased use of artificial intelligence will make the world a safer place.",
    'I trust a self driving car to drive safer than I would normally.',
    "I trust artificial intelligence.",
    "I trust companies that do not use AI over companies that do.",
    "I would prefer to drive a self-driving car over a regular car.",
    "More vehicles, software, and appliances should make use of AI."
]

def get_subject_label(file):
    """Extract the subject label from a given file path. Raises ValueError if no label is found."""
    match = re.search(r'(s\d{3})', file)
    if match:
        subject_label = match.group(1)
        return subject_label
    else:
        raise ValueError(f"Invalid file path: No subject label found in '{file}'")
    
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
    """Calculates average pressures at specified intervals until stop onset"""

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
    """Finds the stop-signal reaction time (SSRT)."""
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
        stop_moment_indices = [i for i in range(ssrt_index, len(pressures)) if pressures[i] == MIN_PRESSURE]
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
    """Calculates go task accuracy metrics."""

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

        # Find the proportion of stops before the stop onset
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
            'proportion_stops_before_stop_onset': proportion_stops_before_stop_onset,
            'ssrt': ssrt,
            'ssrt_without_minimum_ssrt': ssrt_no_min
        }
    return trial_results, ssrt_list

def collect_trial_metric(subject, subject_data, measure, aggregate_ai=False):
    """Collects metric for a single subject, handling AI Block aggregation."""
    results = {'non_ai': [], 'ai_failed': [], 'ai_assisted': []}
    for block, block_data in subject_data.items():
        for trial, trial_data in block_data['trial_results'].items():
            if subject in EXCLUSIONS.keys() and trial in EXCLUSIONS[subject] and block in EXCLUSIONS[subject]:
                continue
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

def grab_mean_metric(shared_control_metrics, measure, aggregate_ai=False):
    """Calculates subject-level means for a specified metric."""

    condition_measure = {}
    for subject, subject_data in shared_control_metrics.items():
        results = collect_trial_metric(subject, subject_data, measure, aggregate_ai)
        condition_measure[subject] = {
            'non_ai': np.nanmean(results['non_ai']),
            'ai_failed': np.nanmean(results['ai_failed']),
            'ai_assisted': np.nanmean(results['ai_assisted']),
        }
    return pd.DataFrame(condition_measure).T.sort_index()

def find_sum_of_intervals(trials_list, measures_dict, max_length, subject):
    """Calculate the sum of pressures at specified intervals for trials."""
    # Pad the trials with NaN to make sure they are the same length
    trials = [np.pad(np.array(lst, dtype=float), (0, max_length - len(lst)), constant_values=np.nan) for 
                                    lst in trials_list]
    # Calculate the proportion of 1s at each interval
    counts = np.count_nonzero(~np.isnan(np.vstack(trials)), axis=0)  # Count valid entries
    measures_dict[subject] = np.nansum(np.vstack(trials) == MAX_PRESSURE, axis=0) / counts # Count number of pressures=1
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

def grab_mean_metric_by_halves(shared_control_metrics, measure):
    """Calculates mean metrics split by trial halves."""
    condition_measure_first_half = {}
    condition_measure_second_half = {}

    for subject, subject_data in shared_control_metrics.items():
        non_ai_first, non_ai_second = [], []
        ai_failed_first, ai_failed_second = [], []
        ai_assisted_first, ai_assisted_second = [], []

        for block, block_data in subject_data.items():
            trial_results = block_data['trial_results']
            num_trials = len(trial_results)

            for i, trial in enumerate(trial_results): # use enumerate directly on trial_results
                if subject in EXCLUSIONS.keys() and trial in EXCLUSIONS[subject] and block in EXCLUSIONS[subject]: # improved exclusion check
                    continue

                ssrt_value = shared_control_metrics[subject][block]['trial_results'][trial][measure]
                if pd.isna(ssrt_value):
                    continue

                if block == 'Non-AI':
                    (non_ai_first if i < num_trials / 2 else non_ai_second).append(ssrt_value)
                elif block == 'AI':
                    condition = shared_control_metrics[subject][block]['trial_results'][trial]['condition']
                    if condition == 'AI-failed':
                        (ai_failed_first if i < num_trials / 2 else ai_failed_second).append(ssrt_value)
                    elif condition == 'AI-assisted':
                        (ai_assisted_first if i < num_trials / 2 else ai_assisted_second).append(ssrt_value)

        condition_measure_first_half[subject] = {
            'non_ai': np.nanmean(non_ai_first),
            'ai_failed': np.nanmean(ai_failed_first),
            'ai_assisted': np.nanmean(ai_assisted_first)
        }
        condition_measure_second_half[subject] = {
            'non_ai': np.nanmean(non_ai_second),
            'ai_failed': np.nanmean(ai_failed_second),
            'ai_assisted': np.nanmean(ai_assisted_second)
        }

    df_first_half = pd.DataFrame(condition_measure_first_half).T.sort_index()
    df_second_half = pd.DataFrame(condition_measure_second_half).T.sort_index()
    return df_first_half, df_second_half

def convert_to_milliseconds(df):
    """Converts specified columns of a DataFrame to milliseconds."""
    for col in ['non_ai', 'ai_failed', 'ai_assisted']:
        if col in df.columns:
            df[col] *= SECONDS_TO_MILLISECONDS

def rename_index_column(df):
    df.rename_axis('subject_id', inplace=True)

def cohens_d_paired(x1, x2):
    """Calculate Cohen's d for paired samples (arrays)"""
    d = (x1 - x2).mean() / np.sqrt(((x1 - x2).std(ddof=1) ** 2) / 2)
    return d

def calculate_ci_for_difference(x1, x2):
    """Calculate confidence interval for the mean difference between two paired samples (arrays)"""
    diff = x1 - x2
    n = len(diff)
    mean_diff = np.mean(diff)
    sem = stats.sem(diff)  # Standard error of the mean
    ci = stats.t.interval(CONFIDENCE, n-1, loc=mean_diff, scale=sem)
    return mean_diff, ci

def calc_stats_ind(data1, data2):
    """Calculate t-stat, p-value, Cohen's d, DF, 95% CI for two independent samples (arrays)"""
    t_statistic, p_value = stats.ttest_ind(data1, data2)
    cohens_d = (np.mean(data1) - np.mean(data2)) / np.sqrt(((len(data1)-1)*np.std(data1)**2 + 
                                                            (len(data2)-1)*np.std(data2)**2)/(len(data1)+len(data2)-2))
    print("Independent samples t-test:")
    print(f"  t-statistic = {t_statistic:.2f}")
    print(f"  p-value = {p_value:.3f}")
    print(f"  Cohen's d = {cohens_d:.2f}")


def print_means_t_test(df, condition1, condition2, alpha=0.05):
    """Prints means, t-statistic, and p-value for a paired t-test."""
    mean1 = np.mean(df[condition1])
    mean2 = np.mean(df[condition2])
    t_test = stats.ttest_rel(df[condition1], df[condition2])

    print(f'Mean {condition1}: {mean1:.2f}')
    print(f'Mean {condition2}: {mean2:.2f}')
    print(f"T-statistic: {t_test.statistic:.2f}, p-value: {t_test.pvalue:.2f}")
    print(f"Significant difference ({condition1} vs {condition2})? {'Yes' if t_test.pvalue < alpha else 'No'}")

def print_effect_size_and_ci(df, condition1, condition2):
    """Prints Cohen's d, mean difference, and confidence interval."""
    cohens_d_val = cohens_d_paired(df[condition1], df[condition2])
    mean_diff, ci = calculate_ci_for_difference(df[condition1], df[condition2], CONFIDENCE)

    print(f"Cohen's d: {cohens_d_val:.2f}")
    print(f"Mean difference ({condition1} - {condition2}): {mean_diff:.2f} ms")
    print(f"{CONFIDENCE*100:.0f}% CI: [{ci[0]:.2f}, {ci[1]:.2f}] ms")

def plot_trial_pressure_individual_for_figure_2(trial_data, trial_number, ax, color):
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
        ax.axvline(x=stop_onset_time, color='#377eb8', linestyle='dotted', linewidth=2, label='Stop Onset')
    if ssrt is not None:
        ax.axvline(x=ssrt+stop_onset_time, color='#984ea3', linestyle='dotted', linewidth=2, label='SSRT')
    if stop_moment is not None:
        ax.axvline(x=stop_moment, color='#4daf4a', linestyle='dotted', linewidth=2, label='Pressure on the Keyboard Reached 0')
    if minimum_ssrt is not None:
        ax.axvline(x=minimum_ssrt, color='#f781bf', linestyle='dotted', linewidth=2, label='Minimum SSRT')

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Raw Pressure')
    handles, labels = plt.gca().get_legend_handles_labels() 
  
    # specify order 
    order = [0, 3, 1, 2] 

    # pass handle & labels lists along with order as below 
    plt.legend([handles[i] for i in order], [labels[i] for i in order], loc="lower left") 
    #ax.legend(loc="lower left")
    ax.grid(True)
    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 3.5)
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Major ticks at every second
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))  # Minor ticks at every 100 ms

def create_summary_df_for_figure_3_and_4(df, value_col, custom_names, desired_order):
    """Creates a summary DataFrame for plotting."""
    melted_df = df.melt(id_vars='subject_id', value_vars=list(custom_names.keys()), var_name='Condition', value_name=value_col)
    melted_df['Condition'] = melted_df['Condition'].map(custom_names)

    summary_df = melted_df.groupby('Condition').agg(
        Mean=(value_col, 'mean'),
        SEM=(value_col, stats.sem)
    ).reset_index()

    n = melted_df.groupby('Condition').size()
    df = n - 1
    ci_bounds = stats.t.interval(0.95, df, loc=summary_df['Mean'], scale=summary_df['SEM'])
    summary_df['CI_lower'] = ci_bounds[0]
    summary_df['CI_upper'] = ci_bounds[1]

    summary_df['Condition'] = pd.Categorical(summary_df['Condition'], categories=desired_order, ordered=True)
    summary_df = summary_df.sort_values('Condition').reset_index(drop=True)
    return melted_df, summary_df

def plot_figure_3_and_4(melted_df, summary_df, value_col, ylabel, filename, ylim=None):
    """Generates the plot."""
    plt.figure(figsize=(6, 7))
    sns.barplot(data=summary_df, x='Condition', y='Mean', palette=["teal", "chocolate"], alpha=0.5)

    for subject in melted_df['subject_id'].unique():
        subject_data = melted_df[melted_df['subject_id'] == subject]
        plt.plot(range(len(subject_data)), subject_data[value_col], color='black', alpha=0.2, linewidth=1)

    sns.stripplot(x='Condition', y=value_col, data=melted_df, color='black', alpha=0.3, size=3, jitter=0, zorder=2)

    for index, row in summary_df.iterrows():
        plt.errorbar(x=index, y=row['Mean'],
                     yerr=[[row['Mean'] - row['CI_lower']], [row['CI_upper'] - row['Mean']]],
                     fmt='none', color='black', capsize=5)

    # Significance annotation (adjust values as needed)
    plt.plot([0, 0, 1, 1], [ylim[1] * 0.95, ylim[1] * 0.96, ylim[1] * 0.96, ylim[1] * 0.95], color='black')  # Adjust y-coordinates as needed for annotation
    plt.text(0.5, ylim[1] * 0.965, "***", ha='center', fontsize=16)
    plt.ylim(ylim)
    plt.xlabel('Condition')
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def numeric_sort_key(col_name):
    match = re.match(r'(\d+)-', col_name)  # Extract the number before the hyphen
    if match:
        return int(match.group(1))
    else:
        return 0

def plot_figure_s1(survey_results, output_filename):
    """Plots the survey correlation matrix efficiently."""

    all_survey_data = []
    for subject_id, details in survey_results.items():
        df = pd.DataFrame(details['data'])
        all_survey_data.append(df)

    combined_df = pd.concat(all_survey_data, keys=survey_results.keys(), names=['subject_id', 'index'])
    combined_df = combined_df.reset_index().pivot(index='subject_id', columns='text', values='corrected_value')

    #Handle potential errors if some questions are missing for some subjects
    combined_df = combined_df.dropna()

    #Rename columns (optional - if you want to keep original question names, remove this section)
    new_columns = [f'Q{i+1}' for i in range(len(combined_df.columns))]
    combined_df.columns = new_columns

    #Calculate and plot the correlation matrix efficiently
    correlation_matrix = combined_df.corr()
    cmap = sns.diverging_palette(240, 10, as_cmap=True)
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap=cmap, center=0, square=True,
                cbar_kws={"shrink": .8}, vmin=-1, vmax=1, annot_kws={"size": 10})
    plt.xlabel("Survey Questions")
    plt.ylabel("Survey Questions")
    tick_positions = np.arange(len(new_columns)) + 0.5
    plt.xticks(ticks=tick_positions, labels=new_columns, ha='right')
    plt.yticks(ticks=tick_positions, labels=new_columns)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.show()

def plot_figure_s2(shared_control_metrics, output_filename):
    all_ssrt_data = []
    for subject, subject_data in shared_control_metrics.items():
        results = collect_trial_metric(subject, subject_data, 'ssrt_without_minimum_ssrt', aggregate_ai=False)
        df = pd.DataFrame({
            'subject': subject,
            'ssrt': results['non_ai'] + results['ai_failed'] + results['ai_assisted']
        })
        all_ssrt_data.append(df)

    ssrt_series = pd.concat(all_ssrt_data, ignore_index=True)['ssrt']
    ssrt_series_ms = ssrt_series * SECONDS_TO_MILLISECONDS  # Convert to milliseconds

    #Filter values
    below_threshold_ms = ssrt_series_ms[ssrt_series_ms <= SSRT_THRESHOLD_FIGURE_S2] #Filter values below threshold ms

    plt.figure(figsize=(10, 5))
    plt.hist(below_threshold_ms, bins=np.arange(below_threshold_ms.min(), 530 + 5, 5), alpha=0.7)
    plt.axvline(x=175, color='red', linestyle='dashed', linewidth=1, label='175ms')
    plt.xlabel('SSRT (ms)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.gca().xaxis.set_major_locator(MultipleLocator(50))
    plt.gca().xaxis.set_minor_locator(MultipleLocator(5))
    plt.savefig(output_filename, dpi=300)
    plt.show()

def calculate_confidence_interval_for_figure_s3(data):
    """Calculates the confidence interval, ignoring NaN values."""
    a = np.array(data)
    valid_data = a[~np.isnan(a)]  #Filter out NaNs
    n = len(valid_data)

    if n < 2:  #Need at least 2 data points for CI calculation
        return (np.nan, np.nan)

    m, se = np.mean(valid_data), stats.sem(valid_data)
    h = se * stats.t.ppf((1 + CONFIDENCE) / 2., n - 1)
    return m - h, m + h

def plot_figure_s3(dataframes, labels, colors, output_filename):
    """Plots proportions with confidence intervals."""
    time_intervals = dataframes[0].columns
    plt.figure(figsize=(12, 6))

    for df, label, color in zip(dataframes, labels, colors):
        means = df.loc['mean across all subjects'].values
        cis = []
        for col in time_intervals:
            lower, upper = calculate_confidence_interval_for_figure_s3(df[col])
            cis.append((lower, upper))

        lower_bounds = np.array([ci[0] for ci in cis])
        upper_bounds = np.array([ci[1] for ci in cis])

        plt.errorbar(x=time_intervals, y=means,
                     yerr=[means - lower_bounds, upper_bounds - means],
                     label=label, color=color, marker='o', capsize=5, fmt='o')

    plt.xlabel('Time Intervals (ms)')
    plt.ylabel("Proportion of 1s")
    plt.xticks(rotation=90)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.show()

def plot_figure_s4(survey_results, filename):
    """Generate a grid of bar charts of responses for a list of survey questions."""
    survey_df = pd.DataFrame(survey_results)
    num_questions = len(QUESTION_LIST)
    cols = 3  # Number of columns for the grid
    rows = (num_questions + cols - 1) // cols  # Calculate number of rows needed for the grid

    # Create a figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=(15, rows * 4))
    axes = axes.flatten()  # Flatten the axes array for easy indexing

    for i, column_name in enumerate(QUESTION_LIST):
        if column_name == "I trust companies that do not use AI over companies that do.":
            survey_df[column_name] = 6 - survey_df[column_name]
        numeric_responses = pd.to_numeric(survey_df[column_name], errors='coerce')
        response_counts = np.bincount(numeric_responses.dropna().astype(int), minlength=6)[1:]
        axes[i].bar(np.arange(1, 6), response_counts, color='skyblue', edgecolor='black', alpha=0.7)

        axes[i].set_xticks(np.arange(1, 6))
        axes[i].set_xlabel("Survey Response")
        axes[i].set_ylabel("Frequency")
        axes[i].set_title(f'Q{i + 1}')
        axes[i].grid(axis='y')

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()

def plot_figure_s5(final_aggregated_results, output_filename):
    """Plots SSD differences efficiently."""

    # Efficiently flatten the data using pandas
    melted_df = final_aggregated_results.explode('all_differences').rename(columns={'all_differences': 'Difference'})
    
    # Calculate mean differences per SSD efficiently using pandas
    mean_data = melted_df.groupby('ssd')['Difference'].mean()

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.scatter(melted_df['ssd'], melted_df['Difference'], color='blue', alpha=0.3, s=30)  # Plot individual data points

    plt.plot(mean_data.index, mean_data.values, color='blue', linewidth=2)  # Plot mean differences

    plt.axhline(0, color='red', linestyle='--')
    plt.xticks(np.arange(0, 800, 50))
    plt.xlabel('SSD (ms)')
    plt.yticks(np.arange(-1000, 1250, 250))
    plt.ylabel('Stop failure RT - No-stop RT (ms)')
    plt.legend() # add legend if needed.
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.show()

def convert_formats(data):
    """Recursively converts NumPy arrays and NumPy numeric types to lists within a nested dictionary."""
    if isinstance(data, dict):
        return {k: convert_formats(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_formats(item) for item in data]
    elif isinstance(data, (np.ndarray, np.int64, np.int32, np.float64, np.float32)): #Handles various numpy numeric types
        return data.tolist() if isinstance(data, np.ndarray) else data.item() #Handle numpy numeric types
    elif isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    else:
        return data
    

def convert_formats_back(data):
    """Recursively converts lists to NumPy arrays if appropriate."""
    if isinstance(data, dict):
        return {k: convert_formats_back(v) for k, v in data.items()}
    elif isinstance(data, list):
        #Check if all elements are numbers. If so, convert to numpy array. Otherwise leave as a list
        if all(isinstance(x, (int, float)) for x in data):
            return np.array(data)
        else:
            return [convert_formats_back(item) for item in data] #Recursively convert nested lists/dicts
    else:
        return data