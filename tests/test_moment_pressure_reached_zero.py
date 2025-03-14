import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_moment_pressure_reached_zero

class TestFindMomentPressureReachedZero(unittest.TestCase):

    def test_ssrt_index_is_none(self):
        self.assertEqual(find_moment_pressure_reached_zero(None, [1, 2, 3], [10, 20, 30]), (np.nan, None))

    def test_no_zero_pressure(self):
        ssrt_index = 1
        time_stamps = [1, 2, 3, 4]
        pressures = [10, 20, 30, 40]
        self.assertEqual(find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures), (np.nan, None))


    def test_zero_pressure_found(self):
        ssrt_index = 1
        time_stamps = [1, 2, 3, 4]
        pressures = [10, 0, 30, 40]
        self.assertEqual(find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures), (2, 1))

    def test_zero_pressure_found_later(self):
        ssrt_index = 0
        time_stamps = [1, 2, 3, 4, 5]
        pressures = [10, 20, 30, 0, 0]  #Multiple zeros, should take the first one.
        self.assertEqual(find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures), (4, 3))

    def test_zero_pressure_at_ssrt_index(self):
        ssrt_index = 0
        time_stamps = [1, 2, 3, 4]
        pressures = [0, 10, 20, 30]
        self.assertEqual(find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures), (1, 0))

    def test_empty_pressures(self):
        ssrt_index = 0
        time_stamps = [1, 2, 3]
        pressures = []
        self.assertEqual(find_moment_pressure_reached_zero(ssrt_index, time_stamps, pressures), (np.nan, None))


if __name__ == '__main__':
    unittest.main()