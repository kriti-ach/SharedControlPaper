import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_first_non_zero_pressure_timestamp, find_first_full_pressure_timestamp, MIN_PRESSURE, MAX_PRESSURE

class TestFindFirstPressureTimestamps(unittest.TestCase):

    def test_empty_lists(self):
        pressures = []
        time_stamps = []
        self.assertTrue(np.isnan(find_first_non_zero_pressure_timestamp(pressures, time_stamps)))
        self.assertTrue(np.isnan(find_first_full_pressure_timestamp(pressures, time_stamps)))

    def test_no_non_zero_pressure(self):
        pressures = [0, 0, 0]
        time_stamps = [10, 20, 30]
        self.assertTrue(np.isnan(find_first_non_zero_pressure_timestamp(pressures, time_stamps)))

    def test_first_non_zero_pressure(self):
        pressures = [0, 0.5, 0.7]
        time_stamps = [10, 20, 30]
        self.assertEqual(find_first_non_zero_pressure_timestamp(pressures, time_stamps), 20)

    def test_first_non_zero_pressure_later(self):
        pressures = [0, 0, 0, 0.1]
        time_stamps = [10, 20, 30, 40]
        self.assertEqual(find_first_non_zero_pressure_timestamp(pressures, time_stamps), 40)


    def test_no_full_pressure(self):
        pressures = [0.1, 0.5, 0.9]
        time_stamps = [10, 20, 30]
        self.assertTrue(np.isnan(find_first_full_pressure_timestamp(pressures, time_stamps)))

    def test_first_full_pressure(self):
        pressures = [0, 0, 1]
        time_stamps = [10, 20, 30]
        self.assertEqual(find_first_full_pressure_timestamp(pressures, time_stamps), 30)

    def test_first_full_pressure_at_beginning(self):
        pressures = [1, 0, 0]
        time_stamps = [10, 20, 30]
        self.assertEqual(find_first_full_pressure_timestamp(pressures, time_stamps), 10)

    def test_first_full_pressure_with_duplicates(self):
        pressures = [0, 1, 1, 0]
        time_stamps = [10, 20, 30, 40]
        self.assertEqual(find_first_full_pressure_timestamp(pressures, time_stamps), 20)


if __name__ == '__main__':
    unittest.main()

