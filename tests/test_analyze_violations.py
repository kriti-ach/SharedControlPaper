import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.simple_stop_utils import analyze_violations

class TestAnalyzeViolations(unittest.TestCase):

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=['trialType', 'rt', 'ssd'])
        result_df = analyze_violations(df)
        self.assertEqual(len(result_df), 0)

    def test_multiple_violation(self):
        df = pd.DataFrame({
            'trialType': ['go', 'stop', 'go', 'stop'],
            'rt': [250, 300, 400, 200],
            'ssd': [100, 200, 300, 400]
        })
        result_df = analyze_violations(df)
        self.assertEqual(len(result_df), 2)
        pd.testing.assert_series_equal(result_df['difference'], pd.Series([50.0, -200.0]), check_names=False)
        pd.testing.assert_series_equal(result_df['ssd'], pd.Series([200.0, 400.0]), check_names=False)

    def test_nan_rt_in_stop_trial(self):
        df = pd.DataFrame({
            'trialType': ['go', 'stop', 'go', 'stop'],
            'rt': [250, np.nan, 400, 200],
            'ssd': [100, 200, 300, 400]
        })
        result_df = analyze_violations(df)
        self.assertEqual(len(result_df), 1)
        pd.testing.assert_series_equal(result_df['difference'], pd.Series([-200.0]), check_names=False)
        pd.testing.assert_series_equal(result_df['ssd'], pd.Series([400.0]), check_names=False)

    def test_no_stop_after_go(self):
        df = pd.DataFrame({
            'trialType': ['go', 'go', 'go', 'go'],
            'rt': [250, 300, 400, 500],
            'ssd': [100, 200, 300, 400]
        })
        result_df = analyze_violations(df)
        self.assertEqual(len(result_df), 0) #No violations

    def test_go_after_stop(self):
        df = pd.DataFrame({
            'trialType': ['stop', 'go', 'stop', 'go'],
            'rt': [250, 300, 400, 200],
            'ssd': [100, 200, 300, 400]
        })
        result_df = analyze_violations(df)
        self.assertEqual(len(result_df), 1)
        pd.testing.assert_series_equal(result_df['difference'], pd.Series([100.0]), check_names=False)
        pd.testing.assert_series_equal(result_df['ssd'], pd.Series([300.0]), check_names=False)


if __name__ == '__main__':
    unittest.main()