"""Temperature Conversion Test Module"""
import pytest
from test_utils import setup_test_path

setup_test_path()
from app import convert_temp

def test_convert_temp():
    """Test temperature conversion functionality"""
    print("\n=== Testing Temperature Conversion ===")
    
    test_cases = [
        (0, 'F', 32, '°F', "0°C to Fahrenheit"),
        (25, 'C', 25, '°C', "25°C keep Celsius"),
        (-10, 'F', 14, '°F', "-10°C to Fahrenheit"),
        (37.5, 'F', 99.5, '°F', "37.5°C to Fahrenheit")
    ]
    
    for input_temp, unit, expected_temp, expected_unit, desc in test_cases:
        temp, unit = convert_temp(input_temp, unit)
        print(f"{desc}: {temp}{unit}")
        assert temp == expected_temp
        assert unit == expected_unit

def test_temp_error_handling():
    """Test temperature conversion error handling"""
    print("\n=== Testing Temperature Conversion Error Handling ===")
    try:
        convert_temp(20, 'K')
    except ValueError as e:
        print(f"Expected error: {e}")
    with pytest.raises(ValueError):
        convert_temp(20, 'K') 