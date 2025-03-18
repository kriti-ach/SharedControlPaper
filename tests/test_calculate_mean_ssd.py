import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import calculate_mean_ssd

class TestCalculateMeanSSD(unittest.TestCase):

    def test_single_condition_all_numbers(self):
        results = {'condition1': [10, 20, 30]}
        self.assertEqual(calculate_mean_ssd(results), 20.0)

    def test_multiple_conditions_all_numbers(self):
        results = {'condition1': [10, 20, 30], 'condition2': [40, 50, 60]}
        self.assertEqual(calculate_mean_ssd(results), 35.0)

    def test_empty_condition(self):
        results = {'condition1': [], 'condition2': [40, 50, 60]}
        self.assertEqual(calculate_mean_ssd(results), 50.0)

    def test_mixed_empty_and_data(self):
        results = {'condition1': [10, 20], 'condition2': []}
        self.assertEqual(calculate_mean_ssd(results), 15.0)


    def test_one_condition_with_data(self):
        results = {'condition1': [10]}
        self.assertEqual(calculate_mean_ssd(results), 10.0)


    def test_with_zeros(self):
        results = {'condition1': [0,0,0], 'condition2': [10,20,30]}
        self.assertEqual(calculate_mean_ssd(results), 10.0)


if __name__ == '__main__':
    unittest.main()