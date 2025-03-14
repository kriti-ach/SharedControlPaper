import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_duration_of_inhibition

class TestFindDurationOfInhibition(unittest.TestCase):

    def test_ssrt_is_nan(self):
        self.assertTrue(np.isnan(find_duration_of_inhibition(np.nan, 5)))

    def test_pressure_reached_zero_is_none(self):
        self.assertTrue(np.isnan(find_duration_of_inhibition(5, None)))

    def test_both_ssrt_and_pressure_are_valid(self):
        ssrt = 2
        pressure_reached_zero = 5
        self.assertEqual(find_duration_of_inhibition(ssrt, pressure_reached_zero), 3)

    def test_pressure_reached_zero_is_smaller_than_ssrt(self):
        ssrt = 5
        pressure_reached_zero = 2
        self.assertEqual(find_duration_of_inhibition(ssrt, pressure_reached_zero), -3)

    def test_both_ssrt_and_pressure_reached_zero_are_floats(self):
        ssrt = 2.5
        pressure_reached_zero = 5.5
        self.assertEqual(find_duration_of_inhibition(ssrt, pressure_reached_zero), 3.0)


if __name__ == '__main__':
    unittest.main()