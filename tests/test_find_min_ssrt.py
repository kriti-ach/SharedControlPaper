import unittest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import find_min_ssrt

class TestFindMinSSRT(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(find_min_ssrt([], 5), (5.175, None)) #stop_onset + MINIMUM_SSRT, None

    def test_min_ssrt_not_found(self):
        time_stamps = [1, 2, 3, 4]
        stop_onset = 5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.175, None))

    def test_min_ssrt_found_at_beginning(self):
        time_stamps = [5.175, 6, 7, 8]  
        stop_onset = 5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.175, 0))

    def test_min_ssrt_found_in_middle(self):
        time_stamps = [1, 2, 5.175, 6, 7] 
        stop_onset = 5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.175, 2))

    def test_min_ssrt_found_at_end(self):
        time_stamps = [1, 2, 3, 5.175] 
        stop_onset = 5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.175, 3))

    def test_stop_onset_and_timestamps_are_floats(self):
        time_stamps = [1.1, 2.2, 3.3, 5.676]
        stop_onset = 5.5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.675, 3))

    def test_min_ssrt_slightly_larger_than_timestamp(self):
        time_stamps = [5.3, 6, 7, 8]
        stop_onset = 5
        self.assertEqual(find_min_ssrt(time_stamps, stop_onset), (5.175, 0))


if __name__ == '__main__':
    unittest.main()
