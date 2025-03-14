import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_stop_onset_idx

class TestFindStopOnsetIdx(unittest.TestCase):

    def test_empty_list(self):
        self.assertIsNone(find_stop_onset_idx([], 5))

    def test_stop_onset_not_found(self):
        time_stamps = [1, 2, 3, 4]
        stop_onset = 5
        self.assertIsNone(find_stop_onset_idx(time_stamps, stop_onset))

    def test_stop_onset_found_at_beginning(self):
        time_stamps = [5, 6, 7, 8]
        stop_onset = 5
        self.assertEqual(find_stop_onset_idx(time_stamps, stop_onset), 0)

    def test_stop_onset_found_in_middle(self):
        time_stamps = [1, 2, 5, 6, 7]
        stop_onset = 5
        self.assertEqual(find_stop_onset_idx(time_stamps, stop_onset), 2)

    def test_stop_onset_found_at_end(self):
        time_stamps = [1, 2, 3, 5]
        stop_onset = 5
        self.assertEqual(find_stop_onset_idx(time_stamps, stop_onset), 3)

    def test_stop_onset_is_float(self):
        time_stamps = [1.1, 2.2, 3.3, 5.5]
        stop_onset = 5.5
        self.assertEqual(find_stop_onset_idx(time_stamps, stop_onset),3)


if __name__ == '__main__':
    unittest.main()