"""Weather Analysis Module

This module provides weather data processing and analysis functionality.

Main features:
    - Temperature unit conversion
    - Weather data analysis
    - Comfort level calculation
    - Weather trend prediction
    - Warning information generation

Functions:
    convert_temp(temp: float, unit: str) -> tuple[float, str]: Temperature unit conversion
    analyze_weather(forecast_data: list, temp_unit: str = 'C') -> dict: Weather data analysis
    get_comfort_emoji(level: str) -> str: Get comfort level emoji
"""

def convert_temp(temp: float, unit: str) -> tuple[float, str]:
    """Temperature unit conversion
    
    Convert Celsius to specified unit.
    
    Args:
        temp: Temperature value (Celsius)
        unit: Target unit ('C' or 'F')
        
    Returns:
        tuple: (Converted temperature, Unit symbol)
    
    Examples:
        >>> convert_temp(25, 'F')
        (77.0, '°F')
    """
    if unit == 'F':
        return (temp * 9/5 + 32, '°F')
    return (temp, '°C')

def analyze_weather(forecast_data, temp_unit='C'):
    """Analyze weather data and return trends and suggestions"""
    temps = [item['main']['temp'] for item in forecast_data]
    humidities = [item['main']['humidity'] for item in forecast_data]
    
    temp_trend = "Stable"
    temp_diff = max(temps) - min(temps)
    
    if temp_unit == 'F':
        display_temp_diff = temp_diff * 9/5
    else:
        display_temp_diff = temp_diff

    if temp_diff > 8:
        temp_trend = "Large Temperature Gap"
    elif temp_diff > 5:
        temp_trend = "Temperature Fluctuation"
    
    comfort_levels = []
    for temp, humidity in zip(temps, humidities):
        if temp < 15:
            comfort_levels.append("Cold")
        elif temp < 20:
            if humidity > 70:
                comfort_levels.append("Cool & Humid")
            else:
                comfort_levels.append("Cool & Comfortable")
        elif temp < 26:
            if humidity > 70:
                comfort_levels.append("Mild & Humid")
            elif humidity < 40:
                comfort_levels.append("Mild & Dry")
            else:
                comfort_levels.append("Comfortable")
        elif temp < 30:
            if humidity > 70:
                comfort_levels.append("Warm & Humid")
            else:
                comfort_levels.append("Warm")
        elif temp < 35:
            if humidity > 60:
                comfort_levels.append("Hot & Humid")
            else:
                comfort_levels.append("Hot")
        else:
            comfort_levels.append("Extremely Hot")
    
    return {
        'temp_trend': temp_trend,
        'comfort_levels': comfort_levels,
        'temp_diff': display_temp_diff
    }

def get_comfort_emoji(level: str) -> str:
    """Get emoji based on comfort level"""
    emoji_map = {
        "Comfortable": "😊",
        "Mild & Dry": "😌",
        "Mild & Humid": "😅",
        "Cool & Comfortable": "🙂",
        "Cool & Humid": "😕",
        "Cold": "🥶",
        "Warm": "😎",
        "Warm & Humid": "😓",
        "Hot": "🥵",
        "Hot & Humid": "😰",
        "Extremely Hot": "🔥"
    }
    return emoji_map.get(level, "😐") 