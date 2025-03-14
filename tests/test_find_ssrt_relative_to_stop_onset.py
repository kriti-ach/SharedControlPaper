import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_ssrt_relative_to_stop_onset

class TestFindSSRTRelativeToStopOnset(unittest.TestCase):

    def test_stop_onset_is_none(self):
        self.assertTrue(np.isnan(find_ssrt_relative_to_stop_onset(np.nan, None)))
        self.assertEqual(find_ssrt_relative_to_stop_onset(5, None), 5)


    def test_ssrt_is_nan(self):
        self.assertTrue(np.isnan(find_ssrt_relative_to_stop_onset(np.nan, 5)))

    def test_both_values_are_valid(self):
        ssrt = 10
        stop_onset = 5
        self.assertEqual(find_ssrt_relative_to_stop_onset(ssrt, stop_onset), 5)

    def test_both_values_are_floats(self):
        ssrt = 10.5
        stop_onset = 5.5
        self.assertEqual(find_ssrt_relative_to_stop_onset(ssrt, stop_onset), 5.0)

    def test_ssrt_is_smaller_than_stop_onset(self):
        ssrt = 5
        stop_onset = 10
        self.assertEqual(find_ssrt_relative_to_stop_onset(ssrt, stop_onset), -5)


if __name__ == '__main__':
    unittest.main()