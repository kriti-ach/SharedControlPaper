import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import calculate_proportions_non_nan

class TestCalculateProportionsNonNan(unittest.TestCase):

    def test_empty_results(self):
        results = {}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {})
        self.assertEqual(total_counts, {})

    def test_all_non_nan(self):
        results = {'condition1': [1, 2, 3], 'condition2': [4, 5, 6]}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {'condition1': 3, 'condition2': 3})
        self.assertEqual(total_counts, {'condition1': 3, 'condition2': 3})

    def test_all_nan(self):
        results = {'condition1': [np.nan, np.nan, np.nan], 'condition2': [np.nan, np.nan, np.nan]}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {'condition1': 0, 'condition2': 0})
        self.assertEqual(total_counts, {'condition1': 3, 'condition2': 3})

    def test_mixed_nan(self):
        results = {'condition1': [1, np.nan, 3], 'condition2': [np.nan, 5, np.nan]}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {'condition1': 2, 'condition2': 1})
        self.assertEqual(total_counts, {'condition1': 3, 'condition2': 3})

    def test_single_condition(self):
        results = {'condition1': [1, np.nan, 3]}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {'condition1': 2})
        self.assertEqual(total_counts, {'condition1': 3})

    def test_with_zero(self):
        results = {'condition1': [0, np.nan, 0]}
        counts, total_counts = calculate_proportions_non_nan(results)
        self.assertEqual(counts, {'condition1': 2})
        self.assertEqual(total_counts, {'condition1': 3})

if __name__ == '__main__':
    unittest.main()