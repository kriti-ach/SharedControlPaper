import numpy as np
import re
from matplotlib.ticker import MultipleLocator
import pandas as pd

def get_subject_label(file):
    """
    Extract the subject label from a given file path.

    Parameters:
    - file (str): The file path from which to extract the subject label.

    Returns:
    - str or None: The extracted subject label (e.g., 's001') if found, 
                   otherwise returns None and prints a message.
    """
    
    match = re.search(r'/sub-(s\d{3})/', file)
    
    if match:
        subject_label = match.group(1)
        return subject_label
    else:
        return None
    

def string_to_numbers(string_data):
    """
    Convert a string of numbers into a list of floats.
    
    Parameters:
    - string_data (str or float): A string containing space-separated numbers or a single float.
    
    Returns:
    - List: A list of floats converted from the input string or a list containing 
      the float if the input is already a float.
    """
    if isinstance(string_data, float):
        return [string_data]
    string_data = string_data.strip("'")
    numbers = [float(num) for num in string_data.split()]
    return numbers

def calculate_intervals(time_stamps, pressures, stop_onset, interval_duration=0.1):
    """
    Calculate accuracies, pressures, and stops at specified intervals until a given endpoint.

    Parameters:
    - time_stamps: Array of timestamps
    - pressures: Array of raw pressure values
    - stop_onset: The point in time when the stop signal appears
    - interval_duration: The duration of each interval in seconds (default 0.1)

    Returns:
    - pressures_at_intervals: List of average pressures at each interval
    """
    pressures_at_intervals = []

    interval_start_idx = 0
    interval_end_time = time_stamps[0] + interval_duration  # Start of the first interval

    while interval_start_idx < len(time_stamps) and time_stamps[interval_start_idx] <= stop_onset:
        temp_pressures = []
        count = interval_start_idx  # Tracks the timestamps within the current interval

        # Loop through timestamps within the current interval
        while (count < len(time_stamps) and 
               time_stamps[count] <= interval_end_time and 
               time_stamps[count] < stop_onset):
            pressure = pressures[count]
            temp_pressures.append(pressure)
            count += 1
        # Calculate average pressure for this interval
        avg_pressure = np.mean(temp_pressures) if temp_pressures else np.nan
        pressures_at_intervals.append(avg_pressure)

        # Move to the next interval if the interval start index is not already count (to ensure it doesn't get stuck in an infinite loop)
        if interval_start_idx != count:
            interval_start_idx = count
        else:
            break
        interval_end_time += interval_duration  # Move the interval end time by specified duration

    return pressures_at_intervals

def process_trial_data(data, block, min_delay=0.175, threshold_reduction=0.30):
    """
    Process trial data for a specific block, calculating metrics including SSRT,
    moment of inhibition, and pressure measures.

    Parameters:
    - data (DataFrame): A DataFrame containing trial data, including pressure, timestamps, and stop signal data.
    - block (str): The block type (e.g., 'AI', 'Non-AI') of the trials to process.
    - min_delay (float): Minimum delay after the stop signal before checking for inhibition (default is 0.175 seconds).
    - threshold_reduction (float): The percentage reduction below which pressure is considered as decreased (default is 30%).

    Returns:
    - trial_results (dict): A dictionary containing various calculated metrics for each trial.
    - ssrt_list (list): A list of SSRT values calculated for each trial.
    """
    trial_results = {}
    ssrt_list = []

    for idx, row in data.iterrows():
        trial_number = idx
        stop_onset = row['SSD']
        time_stamps = row['time_stamps']
        pressures = row['pressures']
        condition = row['condition']
        distances = row['distances']

        if stop_onset is not None:
            stop_onset_idx = next((i for i, t in enumerate(time_stamps) if t >= stop_onset), None)
        else:
            stop_onset_idx = None

        # Calculate the minimum time to start checking for inhibition
        minimum_ssrt = stop_onset + min_delay
        # Find the index to start checking for inhibition (first index after the start_check_time, aka minimum SSRT)
        index_of_minimum_ssrt = next((i for i, t in enumerate(time_stamps) if t >= minimum_ssrt), None)

        ssrt = np.nan 
        index_of_ssrt = None # Index of SSRT
        ssrt_without_minimum_ssrt = np.nan # SSRT calculated without the minimum SSRT period of 175ms
        stop_moment = None # Moment where prssure becomes 0 after the SSRT
        stop_moment_idx = None # Index of the stop moment
        duration_of_inhibition = np.nan # Time between SSRT and the stop moment

        # Find the SSRT and the pressure at the SSRT.
        if index_of_minimum_ssrt is not None:
            for i in range(index_of_minimum_ssrt, len(pressures)):
                current_pressure = pressures[i]
                target_pressure = current_pressure * (1 - threshold_reduction)
                # Check if we have at least 5 more points to examine
                if i + 5 <= len(pressures):
                    # Check monotonic decrease with special case for pressure of 1
                    is_monotonic = True
                    has_thirty_percent_drop = False
                    for j in range(i+1, i+5):
                        if pressures[j-1] == 1.0:
                            if pressures[j] == 1.0: # Break if any of the next 5 timepoints have a pressure = 1
                                is_monotonic = False
                                break
                        else:
                            if pressures[j] > pressures[j-1]:
                                is_monotonic = False
                                break
                        # Check if pressure dropped by at least 30%
                        if pressures[j] <= target_pressure:
                            has_thirty_percent_drop = True
                if is_monotonic and has_thirty_percent_drop:
                    ssrt = time_stamps[i]
                    index_of_ssrt = i
                    break
        
        # Find the SSRT without the 175ms Minimum SSRT
        if stop_onset_idx is not None:
            for i in range(stop_onset_idx, len(pressures)):
                current_pressure = pressures[i]
                target_pressure = current_pressure * (1 - threshold_reduction)
                # Check if we have at least 5 more points to examine
                if i + 5 <= len(pressures):
                    # Check monotonic decrease with special case for pressure of 1
                    is_monotonic = True
                    has_thirty_percent_drop = False
                    for j in range(i+1, i+5):
                        if pressures[j-1] == 1.0:
                            if pressures[j] == 1.0: # Break if any of the next 5 timepoints have a pressure = 1
                                is_monotonic = False
                                break
                        else:
                            if pressures[j] > pressures[j-1]:
                                is_monotonic = False
                                break
                        # Check if pressure dropped by at least 30%
                        if pressures[j] <= target_pressure:
                            has_thirty_percent_drop = True
                if is_monotonic and has_thirty_percent_drop:
                    ssrt_without_minimum_ssrt = time_stamps[i]
                    break

        if not np.isnan(ssrt_without_minimum_ssrt) and stop_onset is not None:
            ssrt_without_minimum_ssrt = ssrt_without_minimum_ssrt - stop_onset

        # Find the end of inhibition (first zero pressure after the start of inhibition)
        if index_of_ssrt is not None:
            stop_moment_indices = [i for i in range(index_of_ssrt, len(pressures)) if pressures[i] == 0]
            if stop_moment_indices:
                stop_moment = time_stamps[stop_moment_indices[0]]
                stop_moment_idx = stop_moment_indices[0]
                

        # Find the duration of inhibition (time between moment of inhibition and end of inhibition) 
        if not np.isnan(ssrt) and stop_moment is not None:
            duration_of_inhibition = stop_moment - ssrt
                
        # Calculate SSRT relative to the stop onset
        if stop_onset is not None and not np.isnan(ssrt):
            ssrt = ssrt - stop_onset
            ssrt_list.append(ssrt)
        else:
            ssrt = np.nan
            ssrt_list.append(ssrt)

        # Calculate Go Task Accuracy at the Onset of the Stop Signal 1 - fully within the ring, 0 - outside the ring
        critical_distance = 2 - 0.8 # This is the distance that needs to be cleared to be outside the circle
        if stop_onset is not None:
            stop_distance = distances[stop_onset_idx]
            if abs(stop_distance) > critical_distance:
                go_task_accuracy_at_stop_onset = 0
            else:
                go_task_accuracy_at_stop_onset = 1
        else:
            stop_distance = np.nan
        
        # Calculate Go Task Accuracy throughout the task until the Stop Signal Appears 1 - within the ring the whole time,
        # 0 - never in the ring
        # Also find the proportion of times the ball was ahead of or behind the ring before the stop onset
        inside_ring_count = 0
        before_ring_count = 0
        after_ring_count = 0
        count = 0
        if stop_onset is not None:
            while count < stop_onset_idx:
                distance = distances[count]
                if abs(distance) <= critical_distance:
                    inside_ring_count += 1
                elif distance < -critical_distance:
                    before_ring_count += 1
                elif distance > critical_distance:
                    after_ring_count += 1
                count += 1
            go_task_accuracy_before_stop_onset = inside_ring_count / count 
            ball_before_ring_proportion_before_stop_onset = before_ring_count / count
            ball_after_ring_proportion_before_stop_onset = after_ring_count / count
        else:
            go_task_accuracy_before_stop_onset = np.nan
            ball_before_ring_proportion_before_stop_onset = np.nan
            ball_after_ring_proportion_before_stop_onset = np.nan

        # Calculate Go Task Accuracy after the Stop Onset until the end of the task 1 - within the ring the whole time, 
        # 0 - never in the ring
        # Also find the proportion of times the ball was ahead of or behind the ring after the stop onset
        inside_ring_count = 0
        if stop_onset is not None:
            count = stop_onset_idx + 1
            while count < len(distances):
                distance = distances[count]
                if abs(distance) <= critical_distance:
                    inside_ring_count += 1
                elif distance < -critical_distance:
                    before_ring_count += 1
                elif distance > critical_distance:
                    after_ring_count += 1
                count += 1
            go_task_accuracy_after_stop_onset = inside_ring_count / (len(distances) - stop_onset_idx)
            ball_before_ring_proportion_after_stop_onset = before_ring_count / (len(distances) - stop_onset_idx)
            ball_after_ring_proportion_after_stop_onset = after_ring_count / (len(distances) - stop_onset_idx)
        else:
            go_task_accuracy_after_stop_onset = np.nan
            ball_before_ring_proportion_after_stop_onset = np.nan
            ball_after_ring_proportion_after_stop_onset = np.nan

        # Find the pressures at time intervals until stop onset
        pressures_at_intervals_until_stop_onset = calculate_intervals(time_stamps, pressures, stop_onset=stop_onset)


        trial_results[trial_number] = {
            'stop_onset': stop_onset,
            'stop_moment': stop_moment,
            'stop_moment_idx': stop_moment_idx,
            'index_of_ssrt': index_of_ssrt,
            'duration_of_inhibition': duration_of_inhibition,
            'distances': distances,
            'pressures': pressures,
            'time_stamps': time_stamps,
            'condition': condition,
            'minimum_ssrt': minimum_ssrt,
            'go_task_accuracy_at_stop_onset': go_task_accuracy_at_stop_onset,
            'go_task_accuracy_before_stop_onset': go_task_accuracy_before_stop_onset,
            'go_task_accuracy_after_stop_onset': go_task_accuracy_after_stop_onset,
            'ball_before_ring_proportion_before_stop_onset': ball_before_ring_proportion_before_stop_onset,
            'ball_after_ring_proportion_before_stop_onset': ball_after_ring_proportion_before_stop_onset,
            'ball_before_ring_proportion_after_stop_onset': ball_before_ring_proportion_after_stop_onset,
            'ball_after_ring_proportion_after_stop_onset': ball_after_ring_proportion_after_stop_onset,
            'pressures_at_intervals_until_stop_onset': pressures_at_intervals_until_stop_onset,
            'ssrt': ssrt,
            'ssrt_without_minimum_ssrt': ssrt_without_minimum_ssrt
        }
    return trial_results, ssrt_list

def find_sum_of_intervals(trials_list, measures_dict, max_length, subject):
    """
    Calculate the sum of pressures at specified intervals for trials.

    Parameters:
    - trials_list (list): A list of arrays containing trial data for a particular condition.
    - measures_dict (dict): A dictionary to store the calculated means/sums for each subject.
    - counts_dict (dict, optional): A dictionary to store counts of valid trial entries for each subject.
    - max_length (int): The max length of a trial between all three conditions.
    - subject (String): The subject ID

    Returns:
    - measures_dict: Updated measures_dict with the calculated values for each subject.
    """
    # Pad the trials with NaN to make sure they are the same length
    trials = [np.pad(np.array(lst, dtype=float), (0, max_length - len(lst)), constant_values=np.nan) for 
                                    lst in trials_list]
    # Calculate the proportion of 1s at each interval
    counts = np.count_nonzero(~np.isnan(np.vstack(trials)), axis=0)  # Count valid entries
    measures_dict[subject] = np.nansum(np.vstack(trials) == 1, axis=0) / counts # Count number of pressures=1
    return measures_dict

def convert_dict_to_df(dict, time_intervals):
    """
    Convert a dictionary into a DataFrame, dropping NaN-only columns and adding mean or sum row.
    
    Parameters:
    - data_dict (dict): The data to convert into a DataFrame.
    - time_intervals (list): List of time interval labels for the columns.
    
    Returns:
    - df: The processed DataFrame.
    """
    df = pd.DataFrame.from_dict(dict, orient='index')
    df = df.dropna(axis=1, how='all')  # Remove columns that are all NaN
    df.columns = time_intervals
    df.index.name = 'subject'
    df = df.sort_values(by='subject')
    df.loc['mean across all subjects'] = df.mean()
    return df

def plot_trial_pressure_individual(trial_data, trial_number, ax, color):
    """
    Function to plot the pressure data for an individual trial. It includes vertical 
    lines marking key events such as stop onset, moment of inhibition, stop moment, 
    and post-buffer stamp.

    Parameters:
    - trial_data (dict): A dictionary containing trial data with keys:
    - trial_number (int): The number of the trial being plotted.
    - ax (matplotlib.axes.Axes): The axes on which to plot the data.
    - color (str): The color to use for the trial plot.
    """
    pressures = trial_data['pressures']
    time_stamps = trial_data['time_stamps']
    stop_onset_time = trial_data.get('stop_onset', None)
    ssrt = trial_data.get('ssrt', None)
    
    stop_moment = trial_data.get('stop_moment', None)
    minimum_ssrt = trial_data.get('minimum_ssrt', None)

    ax.plot(time_stamps, pressures, label=f'Trial {trial_number}', color=color)

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
    ax.legend()
    ax.grid(True)

    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 6.3)
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Major ticks at every second
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))  # Minor ticks at every 100 ms
