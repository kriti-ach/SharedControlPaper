import pandas as pd
import numpy as np
import unittest
from unittest.mock import patch
import io
from sharedcontrolpaper.force_sensitive_stopping_task_utils import print_means_t_test

class TestPrintMeansTTest(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_1(self, stdout):
        df = pd.DataFrame({
            'condition1': [1, 2, 3],
            'condition2': [41, 15, 90]
        })
        print_means_t_test(df, 'condition1', 'condition2')
        expected_output = (
            'Mean condition1: 2.00\n'
            'Mean condition2: 48.67\n'
            "T-statistic: -2.16, p-value: 0.164\n"
            "Significant difference (condition1 vs condition2)? No\n"

        )
        self.assertEqual(stdout.getvalue(), expected_output)