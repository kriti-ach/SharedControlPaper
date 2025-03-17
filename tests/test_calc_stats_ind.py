import pandas as pd
import numpy as np
import unittest
from unittest.mock import patch
import io
from sharedcontrolpaper.force_sensitive_stopping_task_utils import calc_stats_ind


class TestCalcStatsInd(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_basic_calculation(self, stdout):
        data1 = np.array([1, 2, 3, 4, 5])
        data2 = np.array([6, 7, 8, 9, 10, 11])
        calc_stats_ind(data1, data2)
        expected_output = (
            "Independent samples t-test:\n"
            "  t-statistic = -5.20\n"
            "  p-value = 0.001\n"
            "  Cohen's d = -3.47\n"
        )
        self.assertEqual(stdout.getvalue(), expected_output)



if __name__ == '__main__':
    unittest.main()