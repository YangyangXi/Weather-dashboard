"""Weather Analysis Test Module"""
import pytest
from test_utils import setup_test_path

setup_test_path()
from app import analyze_weather, get_comfort_emoji

class TestWeatherAnalysis:
    """Weather Analysis Test Class"""
    
    def test_analyze_weather(self):
        """Test weather analysis functionality"""
        print("\n=== Testing Weather Analysis ===")
        
        # Test normal weather data
        mock_data = [
            {'main': {'temp': 25, 'humidity': 60}},
            {'main': {'temp': 28, 'humidity': 65}},
        ]
        print("\n1. Testing normal weather data:")
        print(f"Input data: {mock_data}")
        result = analyze_weather(mock_data)
        print(f"Analysis result: {result}")
        assert 'temp_trend' in result
        assert 'comfort_levels' in result
        
        # Test large temperature difference
        mock_data_large_diff = [
            {'main': {'temp': 20, 'humidity': 60}},
            {'main': {'temp': 30, 'humidity': 65}},
        ]
        print("\n2. Testing large temperature difference:")
        print(f"Input data: {mock_data_large_diff}")
        result = analyze_weather(mock_data_large_diff)
        print(f"Analysis result: {result}")
        assert result['temp_trend'] == "Large Temperature Gap"
        
        # Test special cases
        self._test_special_cases(mock_data)

    def _test_special_cases(self, mock_data):
        """Test special cases"""
        # Test Fahrenheit unit
        print("\n3. Testing Fahrenheit unit:")
        result = analyze_weather(mock_data, temp_unit='F')
        print(f"Fahrenheit analysis result: {result}")
        assert 'temp_diff' in result
        
        # Test extreme temperatures
        mock_data_extreme = [
            {'main': {'temp': 35, 'humidity': 80}},
            {'main': {'temp': 10, 'humidity': 30}},
        ]
        print("\n4. Testing extreme temperatures:")
        print(f"Input data: {mock_data_extreme}")
        result = analyze_weather(mock_data_extreme)
        print(f"Analysis result: {result}")
        assert "Extremely Hot" in result['comfort_levels']
        assert "Cold" in result['comfort_levels']

class TestComfortLevel:
    """Comfort Level Test Class"""
    
    def test_get_comfort_emoji(self):
        """Test comfort level emoji mapping"""
        print("\n=== Testing Comfort Level Emoji Mapping ===")
        comfort_levels = ["Comfortable", "Cold", "Unknown"]
        for level in comfort_levels:
            emoji = get_comfort_emoji(level)
            print(f"Comfort level '{level}' corresponds to emoji: {emoji}")
            if level == "Comfortable":
                assert emoji == "😊"
            elif level == "Cold":
                assert emoji == "🥶"
            else:
                assert emoji == "😐"

    @pytest.mark.parametrize("temp,humidity,expected", [
        (25, 50, "Comfortable"),
        (15, 40, "Cool & Comfortable"),
        (32, 70, "Hot & Humid"),
        (10, 60, "Cold"),
        (28, 75, "Warm & Humid"),
    ])
    def test_comfort_levels(self, temp, humidity, expected):
        """Parameterized test for comfort level determination with different temperature-humidity combinations"""
        print(f"\nTesting comfort level for temperature {temp}°C, humidity {humidity}%")
        mock_data = [{'main': {'temp': temp, 'humidity': humidity}}]
        result = analyze_weather(mock_data)
        print(f"Analysis result: {result}")
        assert result['comfort_levels'][0] == expected

def test_weather_error_handling():
    """Test weather analysis error handling"""
    print("\n=== Testing Weather Analysis Error Handling ===")
    
    # Test empty data
    print("Testing empty data list:")
    try:
        analyze_weather([])
    except IndexError as e:
        print(f"Expected error (empty data): {e}")
    with pytest.raises(IndexError):
        analyze_weather([])
    
    # Test incorrect data format
    print("\nTesting incorrect data format:")
    try:
        analyze_weather([{'wrong_key': {}}])
    except KeyError as e:
        print(f"Expected error (format error): {e}")
    with pytest.raises(KeyError):
        analyze_weather([{'wrong_key': {}}]) 