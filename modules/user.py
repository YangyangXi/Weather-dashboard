"""User Management Module

This module handles user data management, including user model definition and data persistence.

Main features:
    - User data model
    - User data persistence
    - User information CRUD
    - User preference management

Classes:
    User: User data class
    Login: Login data class

Functions:
    load_users() -> dict: Load user data
    save_users(users_data: dict) -> None: Save user data

Constants:
    DATA_DIR: Data directory path
    USERS_FILE: User data file path
"""

from dataclasses import dataclass
import json
from pathlib import Path

# Create data directory and user data file
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"

# Ensure user data file exists
if not USERS_FILE.exists():
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

@dataclass 
class User:
    """User data class
    
    Attributes:
        name (str): Username
        pwd (str): Password
        city (str): Default city, optional
    """
    name: str
    pwd: str
    city: str = ''

@dataclass
class Login:
    """Login data class
    
    Attributes:
        name (str): Username
        pwd (str): Password
    """
    name: str
    pwd: str

def load_users() -> dict:
    """Load user data
    
    Load user data from JSON file.
    
    Returns:
        dict: User data dictionary
    
    Examples:
        >>> users = load_users()
        >>> print(users['admin']['city'])
        'Beijing'
    """
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(users_data: dict) -> None:
    """Save user data
    
    Save user data to JSON file.
    
    Args:
        users_data (dict): User data dictionary to save
    
    Examples:
        >>> users = {'admin': {'name': 'admin', 'pwd': '123456'}}
        >>> save_users(users)
    """
    with open(USERS_FILE, "w") as f:
        json.dump(users_data, f, indent=2) 