import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import calculate_go_task_metrics

class TestCalculateGoTaskMetrics(unittest.TestCase):

    def test_stop_onset_idx_is_none(self):
        relative_distances = [1, 2, 3]
        stop_onset_idx = None
        results = calculate_go_task_metrics(relative_distances, stop_onset_idx)
        self.assertTrue(np.isnan(results['go_task_accuracy_before_stop_onset']))
        self.assertTrue(np.isnan(results['ball_after_ring_proportion_before_stop_onset']))
        self.assertTrue(np.isnan(results['go_task_accuracy_at_stop_onset']))
        self.assertTrue(np.isnan(results['go_task_accuracy_after_stop_onset']))

    def test_simple_case(self):
        relative_distances = [0.5, 1, 1.5, 2]
        stop_onset_idx = 2
        results = calculate_go_task_metrics(relative_distances, stop_onset_idx)
        self.assertEqual(results['go_task_accuracy_before_stop_onset'], 1)
        self.assertEqual(results['ball_after_ring_proportion_before_stop_onset'], 0.0)
        self.assertEqual(results['go_task_accuracy_at_stop_onset'], 0)
        self.assertEqual(results['go_task_accuracy_after_stop_onset'], 0.0)


    def test_all_outside(self):
        relative_distances = [2, 2, 2, 2]
        stop_onset_idx = 2
        results = calculate_go_task_metrics(relative_distances, stop_onset_idx)
        self.assertEqual(results['go_task_accuracy_before_stop_onset'], 0.0)
        self.assertEqual(results['ball_after_ring_proportion_before_stop_onset'], 1.0)
        self.assertEqual(results['go_task_accuracy_at_stop_onset'], 0)
        self.assertEqual(results['go_task_accuracy_after_stop_onset'], 0.0)


    def test_mixed_case(self):
        relative_distances = [0.5, 1.5, 1, 2, 0.8]
        stop_onset_idx = 2
        results = calculate_go_task_metrics(relative_distances, stop_onset_idx)
        self.assertEqual(results['go_task_accuracy_before_stop_onset'], 0.5)
        self.assertEqual(results['ball_after_ring_proportion_before_stop_onset'], 0.5)
        self.assertEqual(results['go_task_accuracy_at_stop_onset'], 1)
        self.assertEqual(results['go_task_accuracy_after_stop_onset'], 0.5)


    def test_stop_onset_at_the_end(self):
      relative_distances = [0.5, 1, 0.1]
      stop_onset_idx = 2
      results = calculate_go_task_metrics(relative_distances, stop_onset_idx)
      self.assertTrue(np.isnan(results['go_task_accuracy_after_stop_onset']))

if __name__ == '__main__':
    unittest.main()