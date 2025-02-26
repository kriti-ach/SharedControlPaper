import numpy as np
import re
from matplotlib.ticker import MultipleLocator

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
        index_of_ssrt_without_minimum_ssrt = np.nan # Index of SSRT without minimum period
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
                    index_of_ssrt_without_minimum_ssrt = i
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
            'ssrt': ssrt,
            'ssrt_without_minimum_ssrt': ssrt_without_minimum_ssrt
        }
    return trial_results, ssrt_list

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

    # Note: We changed the terminology of moment of inhibition to SSRT, stop moment to the moment when the pressure on the keyboard reached 0
    # , and the post buffer stamp to minimum SSRT for the paper.
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
