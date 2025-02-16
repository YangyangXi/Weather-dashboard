# Weather Forecast System

A modern Python-based weather forecast system providing real-time weather information, forecast analysis, and personalized settings.

## Features

### 1. Weather Information
- Real-time weather conditions
- 24-hour forecast
- 5-day weather forecast
- Air Quality Index (AQI)

### 2. Data Visualization
- Temperature trend charts
- Humidity trend charts
- Wind speed charts
- Air pressure charts

### 3. Smart Analysis
- Temperature trend analysis
- Comfort level assessment
- Weather change alerts
- Temperature difference alerts

### 4. Personalization
- Default city settings
- Temperature unit switching
- User preference saving

### 5. User System
- User registration
- Account login
- Settings management

## Technology Stack

### Backend
- Python 3.8+
- FastHTML Web Framework
- JSON Data Storage

### Frontend
- Chart.js Library
- Responsive Layout
- Modern UI Design

### API
- OpenWeather API
  - Real-time weather data
  - Weather forecast data
  - Air quality data

## Project Structure

```
weather-system/
├── app.py              # Main application entry, contains routing and page rendering logic
├── data/               # Data storage directory
│   └── users.json      # User data storage file
├── modules/            # Feature modules directory
│   ├── __init__.py    # Python package identifier
│   ├── auth.py        # User authentication module
│   ├── styles.py      # UI style definitions
│   ├── user.py        # User management module
│   └── weather.py     # Weather analysis module
├── tests/             # Test directory
│   └── test_utils.py  # Utility tests
└── requirements.txt   # Project dependencies
```

## Module Description

### Core Modules

#### app.py
- Application entry point
- Route definitions
- Page rendering logic
- API integration

#### modules/auth.py
- User authentication middleware
- Login status verification
- Access control
- Security validation

#### modules/user.py
- User data model
- Data persistence
- User information management
- Preference storage

#### modules/weather.py
- Weather data analysis
- Temperature unit conversion
- Comfort level calculation
- Weather trend analysis
- Alert generation

#### modules/styles.py
- Custom style definitions
- Dashboard style configuration
- Responsive layout styles

## Installation

### Requirements
- Python 3.10+
- OpenWeather API key
- Modern browser

### Setup Steps
1. Install dependencies
```bash
pip install -r requirements.txt
```

2. Configure API key
```bash
# Add to .env file
OPENWEATHER_API_KEY=your_api_key_here
```

3. Run application
```bash
python app.py
```

## Usage Guide

### Basic Features
- View real-time weather
- Browse weather forecast
- Analyze weather trends
- Set personal preferences

### Advanced Features
- Multi-city switching
- Data visualization
- Smart analysis
- Alert notifications


