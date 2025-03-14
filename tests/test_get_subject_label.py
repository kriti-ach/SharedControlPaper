import pytest
from sharedcontrolpaper.force_sensitive_stopping_task_utils import get_subject_label

def test_get_subject_label_valid():
    """Test with valid file paths."""
    assert get_subject_label("data/sub-s001/file.csv") == "s001"
    assert get_subject_label("sub-s002_data.txt") == "s002"
    assert get_subject_label("s010/another_file.txt") == "s010"
    assert get_subject_label("path/to/sub-s999/my_data.json") == "s999"

def test_get_subject_label_invalid():
    """Test with invalid file paths (expecting ValueError)."""
    with pytest.raises(ValueError):
        get_subject_label("no_subject_label.txt")
    with pytest.raises(ValueError):
        get_subject_label("data/file.csv")
    with pytest.raises(ValueError):
        get_subject_label("sub-invalid.txt")
    with pytest.raises(ValueError):
        get_subject_label("123")