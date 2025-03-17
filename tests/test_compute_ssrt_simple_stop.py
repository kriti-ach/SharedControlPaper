import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.simple_stop_utils import compute_SSRT

class TestComputeSSRT(unittest.TestCase):

    def test_empty_dataframe(self):
        df = pd.DataFrame(columns=['ssd', 'Phase', 'trialType', 'rt'])
        self.assertTrue(np.isnan(compute_SSRT(df)))

    def test_no_stop_trials(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300],
            'Phase': ['test', 'test', 'test'],
            'trialType': ['go', 'go', 'go'],
            'rt': [250, 300, 400]
        })
        self.assertTrue(np.isnan(compute_SSRT(df)))

    def test_no_go_trials(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300],
            'Phase': ['test', 'test', 'test'],
            'trialType': ['stop', 'stop', 'stop'],
            'rt': [250, np.nan, 400]
        })
        self.assertTrue(np.isnan(compute_SSRT(df)))

    def test_simple_case(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300, 150, 100, 200],
            'Phase': ['test', 'test', 'test', 'test', 'test', 'test'],
            'trialType': ['go', 'go', 'go', 'stop', 'go', 'stop'],
            'rt': [250, 300, 400, 350, 200, 300]
        })
        ssrt = compute_SSRT(df)
        #Manual Calculation for this test case:
        avg_ssd = (150 + 200)/2
        p_respond = 1 #Both stop trials have RTs
        nth_index = int(np.rint(p_respond * 4)) -1 #index 3
        sorted_go_rts = pd.Series([200, 250, 300, 400]).sort_values()
        nth_rt = sorted_go_rts.iloc[3]
        expected_ssrt = nth_rt - avg_ssd
        self.assertAlmostEqual(ssrt, expected_ssrt, places=2)

    def test_with_nan_rt(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300, 150],
            'Phase': ['test', 'test', 'test', 'test'],
            'trialType': ['go', 'go', 'go', 'stop'],
            'rt': [250, np.nan, 400, 350]
        })
        ssrt = compute_SSRT(df)
        #Manual Calculation for this test case:
        avg_ssd = 150
        p_respond = 1
        nth_index = int(np.rint(p_respond * 2))-1 #index 1
        sorted_go_rts = pd.Series([250, 1000, 400]).sort_values() #1000 is for the NaN
        nth_rt = sorted_go_rts.iloc[1]
        expected_ssrt = nth_rt - avg_ssd
        self.assertAlmostEqual(ssrt, expected_ssrt, places=2)


    def test_edge_case_p_respond_zero(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300],
            'Phase': ['test', 'test', 'test'],
            'trialType': ['go', 'go', 'stop'],
            'rt': [250, 300, np.nan]
        })
        ssrt = compute_SSRT(df)
        avg_ssd = 300
        p_respond = 0
        nth_index = int(np.rint(p_respond * 2))-1 
        sorted_go_rts = pd.Series([250, 300]).sort_values() 
        nth_rt = sorted_go_rts.iloc[0]
        expected_ssrt = nth_rt - avg_ssd
        self.assertAlmostEqual(ssrt, expected_ssrt, places=2)

    def test_edge_case_p_respond_one(self):
        df = pd.DataFrame({
            'ssd': [100, 200, 300],
            'Phase': ['test', 'test', 'test'],
            'trialType': ['go', 'go', 'stop'],
            'rt': [250, 300, 350]
        })
        ssrt = compute_SSRT(df)
        #Manual Calculation for this test case:
        avg_ssd = 300
        p_respond = 1
        nth_index = int(np.rint(p_respond * 2)) - 1 #index 1
        sorted_go_rts = pd.Series([250, 300]).sort_values()
        nth_rt = sorted_go_rts.iloc[1]
        expected_ssrt = nth_rt - avg_ssd
        self.assertAlmostEqual(ssrt, expected_ssrt, places=2)


if __name__ == '__main__':
    unittest.main()