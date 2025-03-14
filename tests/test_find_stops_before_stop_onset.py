import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_stops_before_stop_onset

class TestFindStopsBeforeStopOnset(unittest.TestCase):

    def test_stop_onset_idx_is_none(self):
        pressures = [1, 2, 3]
        stop_onset_idx = None
        self.assertTrue(np.isnan(find_stops_before_stop_onset(pressures, stop_onset_idx)))

    def test_stop_onset_idx_is_zero(self):
        pressures = [1, 2, 3]
        stop_onset_idx = 0
        self.assertTrue(np.isnan(find_stops_before_stop_onset(pressures, stop_onset_idx)))

    def test_no_zero_pressures(self):
        pressures = [1, 2, 3]
        stop_onset_idx = 3
        self.assertEqual(find_stops_before_stop_onset(pressures, stop_onset_idx), 0.0)

    def test_all_zero_pressures(self):
        pressures = [0, 0, 0]
        stop_onset_idx = 3
        self.assertEqual(find_stops_before_stop_onset(pressures, stop_onset_idx), 1.0)

    def test_some_zero_pressures(self):
        pressures = [0, 2, 0, 3]
        stop_onset_idx = 4
        self.assertEqual(find_stops_before_stop_onset(pressures, stop_onset_idx), 0.5)

    def test_empty_pressures(self):
        pressures = []
        stop_onset_idx = 1
        self.assertTrue(np.isnan(find_stops_before_stop_onset(pressures, stop_onset_idx)))


    def test_stop_onset_idx_is_one(self):
      pressures = [0]
      stop_onset_idx = 1
      self.assertEqual(find_stops_before_stop_onset(pressures, stop_onset_idx),1.0)

if __name__ == '__main__':
    unittest.main()