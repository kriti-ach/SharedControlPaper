import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import collect_trial_metric

class TestCollectTrialMetric(unittest.TestCase):

    def test_empty_subject_data(self):
        subject = 'subject1'
        subject_data = {}
        measure = 'some_metric'
        results = collect_trial_metric(subject, subject_data, measure)
        self.assertEqual(results['non_ai'], [])
        self.assertEqual(results['ai_failed'], [])
        self.assertEqual(results['ai_assisted'], [])

    def test_non_ai_block(self):
        subject = 'subject1'
        subject_data = {
            'Non-AI': {'trial_results': {'trial1': {'some_metric': 10}, 'trial2': {'some_metric': 20}}}
        }
        measure = 'some_metric'
        results = collect_trial_metric(subject, subject_data, measure)
        self.assertEqual(results['non_ai'], [10, 20])
        self.assertEqual(results['ai_failed'], [])
        self.assertEqual(results['ai_assisted'], [])

    def test_ai_block_aggregate(self):
        subject = 'subject1'
        subject_data = {
            'AI': {'trial_results': {'trial1': {'some_metric': 10, 'condition': 'AI-failed'}, 'trial2': {'some_metric': 20, 'condition': 'AI-assisted'}}}
        }
        measure = 'some_metric'
        results = collect_trial_metric(subject, subject_data, measure, aggregate_ai=True)
        self.assertEqual(results['non_ai'], [])
        self.assertEqual(results['ai_failed'], [10, 20])
        self.assertEqual(results['ai_assisted'], [10, 20])

    def test_ai_block_separate(self):
        subject = 'subject1'
        subject_data = {
            'AI': {'trial_results': {'trial1': {'some_metric': 10, 'condition': 'AI-failed'}, 'trial2': {'some_metric': 20, 'condition': 'AI-assisted'}}}
        }
        measure = 'some_metric'
        results = collect_trial_metric(subject, subject_data, measure, aggregate_ai=False)
        self.assertEqual(results['non_ai'], [])
        self.assertEqual(results['ai_failed'], [10])
        self.assertEqual(results['ai_assisted'], [20])

    def test_missing_measure(self):
        subject = 'subject1'
        subject_data = {
            'Non-AI': {'trial_results': {'trial1': {}, 'trial2': {'some_metric': 20}}}
        }
        measure = 'some_metric'
        results = collect_trial_metric(subject, subject_data, measure)
        self.assertTrue(np.isnan(results['non_ai'][0]))
        self.assertEqual(results['non_ai'][1], 20)



if __name__ == '__main__':
    unittest.main()