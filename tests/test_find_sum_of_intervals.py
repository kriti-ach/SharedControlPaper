import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_sum_of_intervals

MAX_PRESSURE = 1

class TestFindSumOfIntervals(unittest.TestCase):

    def test_single_trial_all_max_pressure(self):
        trials_list = [[MAX_PRESSURE] * 5]
        measures_dict = {}
        max_length = 5
        subject = 'subject1'
        result = find_sum_of_intervals(trials_list, measures_dict, max_length, subject)
        np.testing.assert_array_equal(result['subject1'], np.array([1.0] * 5))


    def test_single_trial_no_max_pressure(self):
        trials_list = [[0] * 5]
        measures_dict = {}
        max_length = 5
        subject = 'subject1'
        result = find_sum_of_intervals(trials_list, measures_dict, max_length, subject)
        np.testing.assert_array_equal(result['subject1'], np.array([0.0] * 5))


    def test_multiple_trials_mixed(self):
        trials_list = [[MAX_PRESSURE, 0, MAX_PRESSURE, 0, MAX_PRESSURE], [MAX_PRESSURE, MAX_PRESSURE, 0, 0, 0]]
        measures_dict = {}
        max_length = 5
        subject = 'subject1'
        result = find_sum_of_intervals(trials_list, measures_dict, max_length, subject)
        np.testing.assert_array_equal(result['subject1'], np.array([1.0, 0.5, 0.5, 0.0, 0.5]))

    def test_unequal_trial_lengths(self):
        trials_list = [[MAX_PRESSURE, 0, MAX_PRESSURE], [MAX_PRESSURE, MAX_PRESSURE, 0, 0, 0]]
        measures_dict = {}
        max_length = 5
        subject = 'subject1'
        result = find_sum_of_intervals(trials_list, measures_dict, max_length, subject)
        np.testing.assert_array_equal(result['subject1'], np.array([1.0, 0.5, 0.5, 0.0, 0.0]))

if __name__ == '__main__':
    unittest.main()