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

def process_trial_data(data, block, min_delay=0.15, threshold_reduction=0.30):
    """
    Process trial data for a specific block, calculating metrics including SSRT,
    moment of inhibition, and pressure measures.

    Parameters:
    - data (DataFrame): A DataFrame containing trial data, including pressure, timestamps, and stop signal data.
    - block (str): The block type (e.g., 'ai', 'non_ai') of the trials to process.
    - min_delay (float): Minimum delay after the stop signal before checking for inhibition (default is 0.15 seconds).
    - threshold_reduction (float): The percentage reduction below which pressure is considered as decreased (default is 30%).

    Returns:
    - trial_results (dict): A dictionary containing various calculated metrics for each trial.
    - ssrt_list (list): A list of SSRT values calculated for each trial.
    """
    trial_results = {}
    ssrt_list = []
    ring_positions_raw = np.arange(-15, 15.0, 0.095).tolist()

    for idx, row in data.iterrows():
        trial_number = idx
        stop_onset = row['SSD_mean']
        time_stamps = row['time_stamps_raw']
        pressures_raw = row['pressures_raw']
        condition = row['condition']
        distances_raw = row['distances_raw']

        if stop_onset is not None:
            stop_onset_idx = next((i for i, t in enumerate(time_stamps) if t >= stop_onset), None)
        else:
            stop_onset_idx = None

        # Calculate the minimum time to start checking for inhibition
        start_check_time = stop_onset + min_delay


        # Find the index to start checking for inhibition (first index after the start_check_time, aka minimum SSRT)
        index_of_start_check = next((i for i, t in enumerate(time_stamps) if t >= start_check_time), None)

        index_of_inhibition = None
        stop_moment = None
        stop_moment_idx = None
        moment_of_inhibition = None
        duration_of_inhibition = np.nan
        distance_at_stop_onset = np.nan
        pressure_at_moment_of_inhibition = np.nan
        distance_at_stop_moment = np.nan
        distance_of_inhibition = np.nan

        # Find the moment of inhibition and the pressure at the moment of inhibition.
        if index_of_start_check is not None:
            for i in range(index_of_start_check, len(pressures_raw)):
                current_pressure = pressures_raw[i]
                target_pressure = current_pressure * (1 - threshold_reduction)
                # Check if we have at least 5 more points to examine
                if i + 5 <= len(pressures_raw):
                    # Check monotonic decrease with special case for pressure of 1
                    is_monotonic = True
                    has_thirty_percent_drop = False
                    for j in range(i+1, i+5):
                        if pressures_raw[j-1] == 1.0:
                            if pressures_raw[j] == 1.0: # Break if any of the next 5 timepoints have a pressure = 1
                                is_monotonic = False
                                break
                        else:
                            if pressures_raw[j] > pressures_raw[j-1]:
                                is_monotonic = False
                                break
                        # Check if pressure dropped by at least 30%
                        if pressures_raw[j] <= target_pressure:
                            has_thirty_percent_drop = True
                if is_monotonic and has_thirty_percent_drop:
                    moment_of_inhibition = time_stamps[i]
                    index_of_inhibition = i
                    pressure_at_moment_of_inhibition = pressures_raw[i]
                    break
        
        # Ring position at moment of inhibition is the same as ring position at stop onset
        # distances_raw is calculated for the ball position relative to the ring position
        distance_at_stop_onset = distances_raw[stop_onset_idx] + ring_positions_raw[stop_onset_idx]

        # Find the end of inhibition (first zero pressure after the start of inhibition) and distance at the end of inhibition
        if index_of_inhibition is not None:
            stop_moment_indices = [i for i in range(index_of_inhibition, len(pressures_raw)) if pressures_raw[i] == 0]
            if stop_moment_indices:
                stop_moment = time_stamps[stop_moment_indices[0]]
                stop_moment_idx = stop_moment_indices[0]
                # Ring position at stop moment is the same as ring position at stop onset
                distance_at_stop_moment = distances_raw[stop_moment_idx] + ring_positions_raw[stop_onset_idx]

        # Find the duration of inhibition (time between moment of inhibition and end of inhibition) 
        # and distance of inhibition (distance between stop moment and stop onset)
        if moment_of_inhibition is not None and stop_moment is not None:
            duration_of_inhibition = stop_moment - moment_of_inhibition
            distance_of_inhibition = distance_at_stop_moment - distance_at_stop_onset
                
        # Calculate SSRT 
        if stop_onset is not None and moment_of_inhibition is not None:
            ssrt = moment_of_inhibition - stop_onset
            ssrt_list.append(ssrt)
        else:
            ssrt = np.nan
            ssrt_list.append(ssrt)
        
        # Calculate Go Task Measure at the Onset of the Stop Signal 1 - fully within the ring, 0 - outside the ring
        critical_distance = 2 - 0.8 # This is the distance that needs to be cleared to be outside the circle
        if stop_onset is not None:
            stop_distance = distances_raw[stop_onset_idx]
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
                distance = distances_raw[count]
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
            while count < len(distances_raw):
                distance = distances_raw[count]
                if abs(distance) <= critical_distance:
                    inside_ring_count += 1
                elif distance < -critical_distance:
                    before_ring_count += 1
                elif distance > critical_distance:
                    after_ring_count += 1
                count += 1
            go_task_accuracy_after_stop_onset = inside_ring_count / (len(distances_raw) - stop_onset_idx)
            ball_before_ring_proportion_after_stop_onset = before_ring_count / (len(distances_raw) - stop_onset_idx)
            ball_after_ring_proportion_after_stop_onset = after_ring_count / (len(distances_raw) - stop_onset_idx)
        else:
            go_task_accuracy_after_stop_onset = np.nan
            ball_before_ring_proportion_after_stop_onset = np.nan
            ball_after_ring_proportion_after_stop_onset = np.nan

        trial_results[trial_number] = {
            'stop_onset': stop_onset,
            'stop_moment': stop_moment,
            'stop_moment_idx': stop_moment_idx,
            'moment_of_inhibition': moment_of_inhibition,
            'index_of_inhibition': index_of_inhibition,
            'duration_of_inhibition': duration_of_inhibition,
            'distance_of_inhibition': distance_of_inhibition,
            'pressure_at_moment_of_inhibition': pressure_at_moment_of_inhibition,
            'distances_raw': distances_raw,
            'pressures_raw': pressures_raw,
            'time_stamps_raw': time_stamps,
            'condition': condition,
            'post_buffer_stamp': start_check_time,
            'go_task_accuracy_at_stop_onset': go_task_accuracy_at_stop_onset,
            'go_task_accuracy_before_stop_onset': go_task_accuracy_before_stop_onset,
            'go_task_accuracy_after_stop_onset': go_task_accuracy_after_stop_onset,
            'ball_before_ring_proportion_before_stop_onset': ball_before_ring_proportion_before_stop_onset,
            'ball_after_ring_proportion_before_stop_onset': ball_after_ring_proportion_before_stop_onset,
            'ball_before_ring_proportion_after_stop_onset': ball_before_ring_proportion_after_stop_onset,
            'ball_after_ring_proportion_after_stop_onset': ball_after_ring_proportion_after_stop_onset,
            'ssrt': ssrt
        }
    return trial_results, ssrt_list

def process_trial_data_without_minimum_ssrt(data, exp_stage="final"):
    """
    Process trial data for a specific block, calculating metrics including SSRT,
    moment of inhibition, and pressure measures. This function calculates the moment of inhibition
    without any minimum SSRT (index_of_start_check).

    Parameters:
    - data (DataFrame): A DataFrame containing trial data, including pressure, timestamps, and stop signal data.
    - exp_stage (String): A string which processes trial data for either the "pilot" subjects or the "final" subjects.

    Returns:
    - trial_results (dict): A dictionary containing various calculated metrics for each trial.
    - ssrt_list (list): A list of SSRT values calculated for each trial.
    """
    trial_results = {}
    ssrt_list = []

    for idx, row in data.iterrows():
        trial_number = idx
        stop_onset = row['SSD_mean']    
        time_stamps = row['time_stamps_raw']
        closest_time = min(time_stamps, key=lambda x: abs(x - stop_onset))
        index_of_closest = time_stamps.index(closest_time) # Index of closest time stamp to stop onset
        raw_pressure = row['pressures_raw'][index_of_closest]

        trial_results[trial_number] = {
            'stop_onset': stop_onset,
            'closest_time': closest_time,
            'index_of_closest': index_of_closest,
            'raw_pressure': raw_pressure,
            'distances_raw': row['distances_raw'],
            'pressures_raw': row['pressures_raw'],
            'time_stamps_raw': row['time_stamps_raw'],
            'condition': row['condition']
        }

    for trial_number, trial_data in trial_results.items():
        index_of_closest = trial_data['index_of_closest']
        pressures_raw = trial_data['pressures_raw']
        time_stamps_raw = trial_data['time_stamps_raw']

        found_stop_pressure = None
        stop_moment = None
        for i in range(index_of_closest + 1, len(pressures_raw)):
            if pressures_raw[i] == 0:
                found_stop_pressure = pressures_raw[i]
                stop_moment = time_stamps_raw[i]
                break

        moment_of_inhibition = None
        index_of_inhibition = None
        
        # This is how the moment of inhibition was originally calculated for the pilot subjects in the pre-reg.
        if exp_stage == "pilot":
            if found_stop_pressure is not None:
                for i in range(index_of_closest + 1, len(pressures_raw)):
                    if pressures_raw[i] < pressures_raw[index_of_closest]:
                        moment_of_inhibition = time_stamps_raw[i]
                        index_of_inhibition = i
                        break
        # This is the correct/updated calculation for moment of inhibition
        else:
            if found_stop_pressure is not None:
                for i in range(index_of_closest + 1, len(pressures_raw)):
                    current_pressure = pressures_raw[i]
                    target_pressure = current_pressure * (1 - 0.3)
                    # Check if we have at least 5 more points to examine
                    if i + 5 <= len(pressures_raw):
                        # Check monotonic decrease with special case for pressure of 1
                        is_monotonic = True
                        has_thirty_percent_drop = False
                        for j in range(i+1, i+5):
                            if pressures_raw[j-1] == 1.0:
                                if pressures_raw[j] == 1.0:
                                    is_monotonic = False
                                    break
                            else:
                                if pressures_raw[j] > pressures_raw[j-1]:
                                    is_monotonic = False
                                    break
                            # Check if pressure dropped by at least 30%
                            if pressures_raw[j] <= target_pressure:
                                has_thirty_percent_drop = True
                    if is_monotonic and has_thirty_percent_drop:
                        moment_of_inhibition = time_stamps_raw[i]
                        index_of_inhibition = i
                        break

        trial_data['stop_pressure'] = found_stop_pressure
        trial_data['stop_moment'] = stop_moment
        trial_data['moment_of_inhibition'] = moment_of_inhibition
        trial_data['index_of_inhibition'] = index_of_inhibition

        if stop_onset is not None and moment_of_inhibition is not None:
            trial_data['ssrt'] = moment_of_inhibition - trial_data['stop_onset'] 
            ssrt = moment_of_inhibition - trial_data['stop_onset'] 
            ssrt_list.append(ssrt)
        else:
            ssrt_list.append(np.nan)
            trial_data['ssrt'] = np.nan

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
    pressures_raw = trial_data['pressures_raw']
    time_stamps_raw = trial_data['time_stamps_raw']
    stop_onset_time = trial_data.get('stop_onset', None)
    moment_of_inhibition = trial_data.get('moment_of_inhibition', None)
    
    stop_moment = trial_data.get('stop_moment', None)
    post_buffer_stamp = trial_data.get('post_buffer_stamp', None)

    ax.plot(time_stamps_raw, pressures_raw, label=f'Trial {trial_number}', color=color)

    # Note: We changed the terminology of moment of inhibition to SSRT, stop moment to the moment when the pressure on the keyboard reached 0
    # , and the post buffer stamp to minimum SSRT for the paper.
    if stop_onset_time is not None:
        ax.axvline(x=stop_onset_time, color='black', linestyle='dotted', linewidth=2, label='Stop Onset')
    if moment_of_inhibition is not None:
        ax.axvline(x=moment_of_inhibition, color='green', linestyle='dotted', linewidth=2, label='SSRT')
    if stop_moment is not None:
        ax.axvline(x=stop_moment, color='red', linestyle='dotted', linewidth=2, label='Pressure on the Keyboard Reached 0')
    if post_buffer_stamp is not None:
        ax.axvline(x=post_buffer_stamp, color='purple', linestyle='dotted', linewidth=2, label='Minimum SSRT')

    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Raw Pressure')
    ax.set_title(f'Trial {trial_number}')
    ax.legend()
    ax.grid(True)

    ax.set_ylim(-0.05, 1.1)
    ax.set_xlim(0, 6.3)
    ax.xaxis.set_major_locator(MultipleLocator(1))  # Major ticks at every second
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))  # Minor ticks at every 100 ms
