import unittest
import numpy as np
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_ssrt

class TestFindSSRT(unittest.TestCase):

    def test_no_drop(self):
        time_stamps = [1, 2, 3, 4, 5]
        pressures = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (np.nan, None))

    def test_drop_but_not_monotonic(self):
        time_stamps = [1, 2, 3, 4, 5]
        pressures = [1.0, .8, .9, .7, .6]  #Not monotonic
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (np.nan, None))

    def test_monotonic_drop(self):
        time_stamps = [1, 2, 3, 4, 5, 6]
        pressures = [1.0, .9, .8, .7, .6, .5]
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (1, 0)) #Should return the first timestamp

    def test_drop_after_start_index(self):
        time_stamps = [1, 2, 3, 4, 5, 6]
        pressures = [1.0, 1.0, .9, .8, .7, .6]
        self.assertEqual(find_ssrt(time_stamps, pressures, 2), (np.nan, None)) #Should not find a drop because not enough timepoints after start index

    def test_insufficient_points(self):
        time_stamps = [1, 2]
        pressures = [1.0, .5]
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (np.nan, None))

    def test_partial_drop(self):
        time_stamps = [1, 2, 3, 4, 5, 6]
        pressures = [1.0, .9, .8, .7, .8, .7] 
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (np.nan,None))

    def test_partial_drop_but_enough_timepoints(self):
        time_stamps = [1, 2, 3, 4, 5, 6]
        pressures = [1.0, .9, .8, .7, .6, .7] 
        self.assertEqual(find_ssrt(time_stamps, pressures, 0), (1, 0))

if __name__ == '__main__':
    unittest.main()