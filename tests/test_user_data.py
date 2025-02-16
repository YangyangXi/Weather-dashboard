"""User Data Test Module"""
from test_utils import setup_test_path

setup_test_path()
from app import load_users, save_users

def test_user_data_operations(test_data_dir, mock_users_file):
    """Test user data operations"""
    print("\n=== Testing User Data Operations ===")
    
    # Test loading user data
    users = load_users()
    print(f"Loaded user data: {users}")
    assert "test_user" in users
    assert users["test_user"]["city"] == "Beijing"
    
    # Test saving user data
    new_user = {
        "new_user": {
            "name": "new_user",
            "pwd": "new_pwd",
            "city": "Shanghai"
        }
    }
    users.update(new_user)
    save_users(users)
    print(f"Data after adding new user: {users}")
    
    # Verify data was saved correctly
    updated_users = load_users()
    print(f"Reloaded user data: {updated_users}")
    assert "new_user" in updated_users
    assert updated_users["new_user"]["city"] == "Shanghai" 