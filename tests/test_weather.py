"""Weather Forecast System Test Module"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import convert_temp, analyze_weather, get_comfort_emoji, load_users, save_users
from pathlib import Path
import json

@pytest.fixture
def test_data_dir(tmp_path):
    """Create test data directory"""
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

def test_convert_temp():
    """Test temperature conversion functionality"""
    # Test Celsius to Fahrenheit conversion
    temp, unit = convert_temp(0, 'F')
    assert temp == 32
    assert unit == '°F'
    
    # Test keeping Celsius
    temp, unit = convert_temp(25, 'C')
    assert temp == 25
    assert unit == '°C'
    
    # Test negative temperature conversion
    temp, unit = convert_temp(-10, 'F')
    assert temp == 14
    assert unit == '°F'
    
    # Test decimal temperature
    temp, unit = convert_temp(37.5, 'F')
    assert temp == 99.5
    assert unit == '°F'

def test_analyze_weather():
    """Test weather analysis functionality"""
    # Test normal weather data
    mock_data = [
        {'main': {'temp': 25, 'humidity': 60}},
        {'main': {'temp': 28, 'humidity': 65}},
    ]
    result = analyze_weather(mock_data)
    assert 'temp_trend' in result
    assert 'comfort_levels' in result
    assert len(result['comfort_levels']) == len(mock_data)
    
    # Test large temperature differences
    mock_data_large_diff = [
        {'main': {'temp': 20, 'humidity': 60}},
        {'main': {'temp': 30, 'humidity': 65}},
    ]
    result = analyze_weather(mock_data_large_diff)
    assert result['temp_trend'] == "Large Temperature Gap"
    
    # Test Fahrenheit unit
    result = analyze_weather(mock_data, temp_unit='F')
    assert 'temp_diff' in result
    
    # Test extreme temperatures
    mock_data_extreme = [
        {'main': {'temp': 35, 'humidity': 80}},
        {'main': {'temp': 10, 'humidity': 30}},
    ]
    result = analyze_weather(mock_data_extreme)
    assert "Extremely Hot" in result['comfort_levels']
    assert "Cold" in result['comfort_levels']

def test_get_comfort_emoji():
    """Test comfort level emoji mapping"""
    # Test basic emoji mapping
    assert get_comfort_emoji("Comfortable") == "😊"
    assert get_comfort_emoji("Cold") == "🥶"
    assert get_comfort_emoji("Unknown") == "😐"  # Default emoji
    
    # Test all possible comfort levels
    comfort_levels = [
        "Comfortable", "Mild & Dry", "Mild & Humid", "Cool & Comfortable",
        "Cool & Humid", "Cold", "Warm", "Warm & Humid",
        "Hot", "Hot & Humid", "Extremely Hot"
    ]
    for level in comfort_levels:
        assert get_comfort_emoji(level) != "😐"  # Ensure all valid levels have corresponding emojis

@pytest.mark.parametrize("temp,humidity,expected", [
    (25, 50, "Comfortable"),
    (15, 40, "Cool & Comfortable"),
    (32, 70, "Hot & Humid"),
    (10, 60, "Cold"),
    (28, 75, "Warm & Humid"),
])
def test_comfort_levels(temp, humidity, expected):
    """Parameterized test for comfort level determination"""
    mock_data = [{'main': {'temp': temp, 'humidity': humidity}}]
    result = analyze_weather(mock_data)
    assert result['comfort_levels'][0] == expected

def test_error_handling():
    """Test error handling"""
    # Test invalid temperature unit
    with pytest.raises(ValueError):
        convert_temp(20, 'K')
    
    # Test empty data
    with pytest.raises(IndexError):
        analyze_weather([])
    
    # Test incorrect data format
    with pytest.raises(KeyError):
        analyze_weather([{'wrong_key': {}}]) 