import pandas as pd
import numpy as np
import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import cohens_d_paired

class TestCohensDPaired(unittest.TestCase):

    def test_simple_case(self):
        x1 = np.array([1, 2, 3])
        x2 = np.array([41, 15, 90])
        d = cohens_d_paired(x1, x2)
        self.assertAlmostEqual(d, -1.246, places=3)

if __name__ == '__main__':
    unittest.main()