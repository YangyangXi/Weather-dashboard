"""Test configuration and shared fixtures"""
import pytest
import json
from pathlib import Path
from test_utils import setup_test_path

setup_test_path()

@pytest.fixture
def test_data_dir(tmp_path):
    """Create test data directory（Used to create a temporary test data directory）"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def mock_users_file(test_data_dir):
    """Create test user data file"""
    users_file = test_data_dir / "users.json"
    test_users = {
        "test_user": {
            "name": "test_user",
            "pwd": "test_pwd",
            "city": "Beijing"
        }
    }
    users_file.write_text(json.dumps(test_users))
    return users_file 