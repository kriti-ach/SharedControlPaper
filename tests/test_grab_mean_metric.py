import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import grab_mean_metric

class TestGrabMeanMetric(unittest.TestCase):

    def test_empty_shared_control_metrics(self):
        shared_control_metrics = {}
        measure = 'some_metric'
        df = grab_mean_metric(shared_control_metrics, measure)
        self.assertEqual(len(df), 0)

    def test_simple_case(self):
        shared_control_metrics = {
            'subject1': {
                'Non-AI': {'trial_results': {'trial1': {'some_metric': 10}, 'trial2': {'some_metric': 20}}},
                'AI': {'trial_results': {'trial1': {'some_metric': 30, 'condition': 'AI-failed'}, 'trial2': {'some_metric': 40, 'condition': 'AI-assisted'}}}
            }
        }
        measure = 'some_metric'
        df = grab_mean_metric(shared_control_metrics, measure)
        pd.testing.assert_frame_equal(df, pd.DataFrame({
            'non_ai': [15.0],
            'ai_failed': [30.0],
            'ai_assisted': [40.0]
        }, index=['subject1']))

    def test_with_nan(self):
        shared_control_metrics = {
            'subject1': {
                'Non-AI': {'trial_results': {'trial1': {'some_metric': 10}, 'trial2': {'some_metric': np.nan}}},
                'AI': {'trial_results': {'trial1': {'some_metric': 30, 'condition': 'AI-failed'}, 'trial2': {'some_metric': 40, 'condition': 'AI-assisted'}}}
            }
        }
        measure = 'some_metric'
        df = grab_mean_metric(shared_control_metrics, measure)
        pd.testing.assert_frame_equal(df, pd.DataFrame({
            'non_ai': [10.0],
            'ai_failed': [30.0],
            'ai_assisted': [40.0]
        }, index=['subject1']))

    def test_aggregate_ai(self):
        shared_control_metrics = {
            'subject1': {
                'Non-AI': {'trial_results': {'trial1': {'some_metric': 10}, 'trial2': {'some_metric': 20}}},
                'AI': {'trial_results': {'trial1': {'some_metric': 30, 'condition': 'AI-failed'}, 'trial2': {'some_metric': 40, 'condition': 'AI-assisted'}}}
            }
        }
        measure = 'some_metric'
        df = grab_mean_metric(shared_control_metrics, measure, aggregate_ai=True)
        pd.testing.assert_frame_equal(df, pd.DataFrame({
            'non_ai': [15.0],
            'ai_failed': [35.0],
            'ai_assisted': [35.0]
        }, index=['subject1']))


if __name__ == '__main__':
    unittest.main()