import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import grab_mean_metric_by_halves

class TestGrabMeanMetricByHalves(unittest.TestCase):

    def test_empty_shared_control_metrics(self):
        shared_control_metrics = {}
        measure = 'some_metric'
        df_first, df_second = grab_mean_metric_by_halves(shared_control_metrics, measure)
        self.assertEqual(len(df_first), 0)
        self.assertEqual(len(df_second), 0)

    def test_trials(self):
        shared_control_metrics = {
            'subject1': {
                'Non-AI': {
                    'trial_results': {
                        0: {'some_metric': 10},
                        1: {'some_metric': 20},
                        2: {'some_metric': 30},
                        3: {'some_metric': 40}
                    }
                },
                'AI': {
                    'trial_results': {
                        0: {'some_metric': 50, 'condition': 'AI-failed'},
                        1: {'some_metric': 60, 'condition': 'AI-assisted'},
                        2: {'some_metric': 70, 'condition': 'AI-failed'},
                        3: {'some_metric': 80, 'condition': 'AI-assisted'}
                    }
                }
            }
        }
        measure = 'some_metric'
        df_first, df_second = grab_mean_metric_by_halves(shared_control_metrics, measure)
        pd.testing.assert_frame_equal(df_first, pd.DataFrame({'non_ai': [15.0], 'ai_failed': [50.0], 'ai_assisted': [60.0]}, index=['subject1']))
        pd.testing.assert_frame_equal(df_second, pd.DataFrame({'non_ai': [35.0], 'ai_failed': [70.0], 'ai_assisted': [80.0]}, index=['subject1']))


if __name__ == '__main__':
    unittest.main()