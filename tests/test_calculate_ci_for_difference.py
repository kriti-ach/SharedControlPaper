import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import calculate_ci_for_difference

class TestCiForDifference(unittest.TestCase):

    def test_arrays(self):
        x1 = np.array([1, 2, 3])
        x2 = np.array([41, 15, 90])
        mean_diff, ci = calculate_ci_for_difference(x1, x2)
        self.assertAlmostEqual(mean_diff, -46.666666666666664, places=10)
        self.assertAlmostEqual(ci, (-139.6920132099643, 46.358679876630966))

if __name__ == '__main__':
    unittest.main()