"""Weather Forecast System Main Application

This module is the entry point for the application, containing route definitions and page processing logic.

Main features:
    - Route definitions and processing
    - Page rendering
    - API call integration
    - User interaction processing

Routes:
    GET  /: Home page
    GET  /login: Login page
    POST /login: Handle login
    GET  /register: Register page
    POST /register: Handle register
    GET  /dashboard: Dashboard page
    POST /update_settings: Update settings
    GET  /logout: Logout

Dependencies:
    - fasthtml: Web framework
    - httpx: HTTP client
    - modules.user: User management module
    - modules.weather: Weather analysis module
    - modules.auth: Authentication module
    - modules.styles: Style module
"""
from fasthtml.common import *
from dataclasses import dataclass
from hmac import compare_digest
import json
from pathlib import Path
import httpx
from datetime import datetime
# Import custom modules
from modules.user import User, Login, load_users, save_users
from modules.weather import convert_temp, analyze_weather, get_comfort_emoji
from modules.auth import auth_before, login_redir
from modules.styles import custom_style, dashboard_style


# Create user data class
@dataclass 
class User:
    name: str
    pwd: str
    city: str = ''

# Login data class
@dataclass
class Login:
    name: str
    pwd: str

# Redirect response
login_redir = RedirectResponse('/login', status_code=303)

# Authentication middleware
def auth_before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth and req.url.path not in ['/login', '/register']: 
        return login_redir

# Custom style
custom_style = """
:root {
    --primary: #4f46e5;
    --primary-hover: #4338ca;
    --background: #f9fafb;
}

body {
    background: var(--background);
    min-height: 100vh;
}
"""

# Use separate string to define dashboard style
dashboard_style = """
.dashboard-container {
    max-width: 800px !important;
    margin: 2rem auto !important;
    padding: 1rem !important;
}

.weather-card {
    margin-bottom: 1.5rem;
}

.weather-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.weather-item {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    transition: transform 0.2s;
}

.weather-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

.weather-item h3 {
    color: var(--primary);
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
}

.weather-item p {
    margin: 0.5rem 0;
    color: #374151;
}

.settings-form {
    padding: 1.5rem;
}

.settings-form .input-group {
    margin-bottom: 1.5rem;
}

.radio-group {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
}

.radio-group label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
}

.save-btn {
    background: var(--primary);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
}

.save-btn:hover {
    background: var(--primary-hover);
    transform: translateY(-1px);
}

.weather-section-title {
    color: var(--primary);
    padding: 1rem;
    margin: 1rem 0 0.5rem 0;
    border-bottom: 1px solid #e5e7eb;
}

.nav-tabs {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 1rem;
}

.nav-tab {
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    color: #6b7280;
    background: #f3f4f6;
    transition: all 0.2s;
}

.nav-tab:hover {
    background: #e5e7eb;
    color: #374151;
}

.nav-tab.active {
    background: var(--primary);
    color: white;
}

.tab-content {
    display: none;
}

.tab-content.active {
    display: block;
}

.search-container {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.search-form {
    display: flex;
    align-items: center;
    gap: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

.search-input {
    flex: 1;
    height: px;  /* Fixed height */
    padding: 0 1.2rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.2s;
}

.search-input:focus {
    border-color: var(--primary);
    outline: none;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.search-btn {
    height: 44px;  /* Same height as input box */
    padding: 0 2rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;  /* Prevent text from wrapping */
}

.search-btn:hover {
    background: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.weather-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.forecast-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 1rem;
    overflow-x: auto;
    padding: 1rem;
}

.forecast-item {
    text-align: center;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 8px;
    min-width: 120px;
}

.forecast-item h4 {
    margin: 0;
    color: var(--primary);
}

.weather-icon {
    font-size: 2rem;
    margin: 0.5rem 0;
}

.trend-chart {
    width: 100%;
    height: 300px;
    margin: 1rem 0;
}

.weather-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    padding: 1rem;
    background: #f8fafc;
    border-radius: 8px;
}

.detail-item {
    text-align: center;
    padding: 0.5rem;
}

.detail-item h4 {
    margin: 0;
    color: var(--primary);
}

.weather-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.info-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s;
}

.info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    padding: 1.5rem;
    border-radius: 12px 12px 0 0;
}

.card-header h2 {
    color: white;
    margin: 0;
    font-size: 1.5rem;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.card-content {
    padding: 1.5rem;
}

.weather-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
}

.info-item {
    background: #f8fafc;
    padding: 1.25rem;
    border-radius: 8px;
    text-align: center;
}

.info-item h3 {
    color: var(--primary);
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
}

.info-item p {
    color: #374151;
    font-size: 1.1rem;
}

.main-temp {
    font-size: 2.5rem !important;
    font-weight: bold;
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem !important;
}

.header-actions {
    display: flex;
    gap: 1.5rem;  /* Increased button spacing */
    align-items: center;
}

.header-btn {
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.2s;
    font-weight: 500;
}

.settings-btn {
    background: white;
    color: var(--primary);
    border: 2px solid var(--primary);
}

.settings-btn:hover {
    background: var(--primary);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.logout-btn {
    background: #ef4444;
    color: white;
    border: none;
}

.logout-btn:hover {
    background: #dc2626;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(239, 68, 68, 0.2);
}

.location-header {
    color: var(--primary);
    font-size: 1.25rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary);
}

.charts-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);  /* 2x2 grid */
    gap: 2rem;
    margin: 2rem 0;
}

.chart-wrapper {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.trend-chart {
    width: 100%;
    height: 300px !important;
}

.chart-title {
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.2rem;
    text-align: center;
}

.time-range-selector {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
}

.time-btn {
    padding: 0.5rem 1.5rem;
    border: 2px solid var(--primary);
    border-radius: 8px;
    background: white;
    color: var(--primary);
    cursor: pointer;
    transition: all 0.2s;
}

.time-btn.active {
    background: var(--primary);
    color: white;
}

.time-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    padding: 1.5rem;
}

.analysis-item {
    background: #f8fafc;
    padding: 1.25rem;
    border-radius: 8px;
    transition: transform 0.2s;
}

.analysis-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.analysis-item h3 {
    color: var(--primary);
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.analysis-item p {
    margin: 0.5rem 0;
    color: #374151;
}

.warning {
    background: #fef2f2;
    border: 1px solid #fee2e2;
}

.analysis-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin: 2rem 0;
}

.analysis-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    padding: 1.5rem;
    border-radius: 12px 12px 0 0;
}

.analysis-header h2 {
    color: white;
    margin: 0;
    font-size: 1.5rem;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.analysis-content {
    padding: 1.5rem;
}

.analysis-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.analysis-chart {
    height: 250px !important;
    margin-top: 1rem;
}

.analysis-item {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 12px;
    transition: all 0.2s;
}

.analysis-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
}

.analysis-stat {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.stat-icon {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: var(--primary);
    color: white;
    font-size: 1.2rem;
}

.stat-info h4 {
    margin: 0;
    color: #374151;
}

.stat-info p {
    margin: 0.25rem 0 0 0;
    color: var(--primary);
    font-weight: 500;
}

.warning-list {
    margin-top: 1rem;
}

.warning-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: #fef2f2;
    border-radius: 6px;
    margin-bottom: 0.5rem;
    color: #ef4444;
}

.comfort-timeline {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    padding: 1rem 0;
    margin-top: 1rem;
}

.comfort-point {
    flex: 0 0 auto;
    background: white;
    padding: 1rem 1.5rem;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s;
    min-width: 120px;
}

.comfort-point:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.comfort-time {
    color: var(--primary);
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.comfort-emoji {
    font-size: 1.5rem;
    margin: 0.5rem 0;
}

.comfort-level {
    color: #374151;
}

.auth-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #e0f2fe 0%, #dbeafe 100%);
}

.auth-card {
    width: 100%;
    max-width: 420px;
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    padding: 2rem;
}

.auth-header {
    text-align: center;
    color: var(--primary);
    margin-bottom: 2rem;
    font-size: 1.75rem;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.auth-form .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.auth-form input {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid #e5e7eb;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.2s;
}

.auth-form input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    outline: none;
}

.auth-form button {
    width: 100%;
    padding: 0.875rem;
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.auth-form button:hover {
    background: var(--primary-hover);
    transform: translateY(-1px);
}

.auth-footer {
    margin-top: 1.5rem;
    text-align: center;
}

.auth-footer a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.2s;
}

.auth-footer a:hover {
    color: var(--primary-hover);
    text-decoration: underline;
}

.auth-brand {
    text-align: center;
    margin-bottom: 2rem;
}

.auth-brand h1 {
    color: var(--primary);
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.auth-brand p {
    color: #6b7280;
}

.dashboard-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
    color: white;
    font-size: 1.5rem;
    font-weight: 500;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 1rem;
}

.header-btn {
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s;
    text-decoration: none;
    font-size: 0.95rem;
}

.settings-btn {
    background: #3b82f6 !important;  /* Use !important to prevent override */
    color: white !important;
}

.settings-btn:hover {
    background: #2563eb !important;
    transform: translateY(-1px);
}

.logout-btn {
    background: #ef4444 !important;  /* Use !important to prevent override */
    color: white !important;
}

.logout-btn:hover {
    background: #dc2626 !important;
    transform: translateY(-1px);
}

.page-header {
    text-align: center;
    margin-bottom: 2rem;
}

.page-header h1 {
    color: var(--primary);
    font-size: 2rem;
    font-weight: 600;
    margin: 0;
    padding: 1rem 0;
}

.dashboard-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
    color: white;
    font-size: 1.5rem;
    font-weight: 500;
    margin: 0;
}

.header-actions {
    display: flex;
    gap: 1rem;
}

.header-btn {
    padding: 0.5rem 1.25rem;
    border-radius: 8px;
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
}

.settings-btn {
    background: rgba(255, 255, 255, 0.2);
}

.settings-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
}

.logout-btn {
    background: rgba(239, 68, 68, 0.2);
}

.logout-btn:hover {
    background: rgba(239, 68, 68, 0.3);
    transform: translateY(-1px);
}

.page-title {
    text-align: center;
    color: var(--primary);
    font-size: 2rem;
    font-weight: 600;
    margin: 2rem 0;
    padding: 0.5rem 0;
    letter-spacing: -0.5px;
}
"""

# Create application
app, rt = fast_app(
    before=Beforeware(auth_before),
    hdrs=(
        Style(custom_style),
        Style(dashboard_style),
        Script(src="https://cdn.jsdelivr.net/npm/chart.js"),
    )
)

# Login page
@rt("/login")
def get():
    frm = Form(
        Div(
            Input(id='name', placeholder='Username', required=True),
            cls='input-group'
        ),
        Div(
            Input(id='pwd', type='password', placeholder='Password', required=True),
            cls='input-group'
        ),
        Button('Login', cls='primary'),
        action='/login', method='post',
        cls='auth-form'
    )
    return Titled("", 
        Main(
            Card(
                Div(
                    H1("Weather Forecast System"),
                    P("Stay updated with weather conditions"),
                    cls="auth-brand"
                ),
                H2("Account Login", cls="auth-header"),
                frm,
                Div(
                    A('No account? Register now', href='/register'),
                    cls="auth-footer"
                ),
                cls="auth-card"
            ),
            cls="container auth-container"
        )
    )

# Handle login
@rt("/login") 
def post(login:Login, sess):
    if not login.name or not login.pwd:
        return login_redir
    
    users = load_users()
    if login.name not in users:
        return login_redir
    
    stored_user = users[login.name]
    if not compare_digest(stored_user['pwd'].encode(), login.pwd.encode()):
        return login_redir
    
    sess['auth'] = login.name
    return RedirectResponse('/dashboard', status_code=303)

# Register page
@rt("/register")
def get():
    frm = Form(
        Div(
            Input(id='name', placeholder='Set Username', required=True),
            cls='input-group'
        ),
        Div(
            Input(id='pwd', type='password', placeholder='Set Password', required=True),
            cls='input-group'
        ),
        Div(
            Input(id='city', placeholder='Your City', required=True),
            cls='input-group'
        ),
        Button('Register', cls='primary'),
        action='/register', method='post',
        cls='auth-form'
    )
    return Titled("Register", 
        Main(
            Card(
                Div(
                    H1("Weather Forecast System"),
                    P("Join us on the weather journey"),
                    cls="auth-brand"
                ),
                H2("Create Account", cls="auth-header"),
                frm,
                Div(
                    A('Have an account? Login now', href='/login'),
                    cls="auth-footer"
                ),
                cls="auth-card"
            ),
            cls="container auth-container"
        )
    )

# Handle register
@rt("/register")
def post(user:User):
    if not user.name or not user.pwd:
        return RedirectResponse('/register', status_code=303)
    
    users = load_users()
    if user.name in users:
        return RedirectResponse('/register', status_code=303)
    
    # Convert user data to dictionary and save
    users[user.name] = {
        'name': user.name,
        'pwd': user.pwd,
        'city': user.city
    }
    
    save_users(users)
    return RedirectResponse('/login', status_code=303)

# Update user settings
@rt("/update_settings")
def post(auth, city: str, temp_unit: str):
    users = load_users()
    users[auth]['city'] = city
    users[auth]['temp_unit'] = temp_unit
    save_users(users)
    return RedirectResponse('/dashboard', status_code=303)

# Temperature conversion function
def convert_temp(temp: float, unit: str) -> tuple[float, str]:
    if unit == 'F':
        return (temp * 9/5 + 32, '°F')
    return (temp, '°C')

# Modify weather analysis function
def analyze_weather(forecast_data, temp_unit='C'):
    """Analyze weather data and return trend and suggestion"""
    # Get temperature data, temperature in forecast_data is always in Celsius
    temps = [item['main']['temp'] for item in forecast_data]
    humidities = [item['main']['humidity'] for item in forecast_data]
    
    # Temperature trend analysis
    temp_trend = "Stable"
    temp_diff = max(temps) - min(temps)
    
    # According to temperature unit, set threshold and convert temperature difference
    if temp_unit == 'F':
        display_temp_diff = temp_diff * 9/5  # Only convert display temperature difference
    else:
        display_temp_diff = temp_diff

    if temp_diff > 8:
        temp_trend = "Large Temperature Gap"
    elif temp_diff > 5:
        temp_trend = "Temperature Fluctuation"
    
    # Comfort level calculation (using Celsius)
    comfort_levels = []
    for temp, humidity in zip(temps, humidities):  # temps is already in Celsius
        # Use improved comfort level calculation formula
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

# Dashboard page
@rt("/dashboard")
async def get(auth, tab: str = 'weather', city: str = None, range: str = '24h'):
    users = load_users()
    user = users[auth]
    default_city = user['city']
    temp_unit = user.get('temp_unit', 'C')
    
    # Use searched city or default city
    current_city = city or default_city
    
    try:
        async with httpx.AsyncClient() as client:
            api_key = "ffbd62ce8de707d8aef093dca5dce999"
            
            # Modify search form packaging
            search_form = Div(
                Form(
                    Input(
                        id='search_city',
                        name='search_city',
                        placeholder='Enter city name...',
                        value=current_city,
                        required=True,
                        cls='search-input'
                    ),
                    Button('Search', cls='search-btn'),
                    action='/dashboard/search',
                    method='post',
                    cls='search-form'
                ),
                cls='search-container'
            )

            # 1. Get current weather
            current_resp = await client.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={current_city}&appid={api_key}&units=metric&lang=en",
                timeout=10.0
            )
            
            if current_resp.status_code != 200:
                raise Exception(f"API returned error: {current_resp.text}")
            
            current = current_resp.json()
            print("Debug - Current weather data:", current)  # Add debug output
            
            # Temperature data processing
            temp = current['main']['temp']
            feels_like = current['main']['feels_like']
            
            # According to user settings, convert temperature unit
            if temp_unit == 'F':
                temp = temp * 9/5 + 32
                feels_like = feels_like * 9/5 + 32
                unit = '°F'
            else:
                unit = '°C'
            
            # Sunrise and sunset time conversion
            sunrise = datetime.fromtimestamp(current['sys']['sunrise']).strftime('%H:%M:%S')
            sunset = datetime.fromtimestamp(current['sys']['sunset']).strftime('%H:%M:%S')
            
            # Current weather card
            current_card = Div(
                Div(
                    H2(f"{current_city} · Current Weather"),  # Changed from 实时天气
                    cls="card-header"
                ),
                Div(
                    Div(
                        Div(
                            H3("Current Temperature"),  # Changed from 当前温度
                            P(f"{temp:.1f}{unit}", cls="main-temp"),
                            P(f"Feels like: {feels_like:.1f}{unit}"),  # Changed from 体感温度
                            cls="info-item"
                        ),
                        Div(
                            H3("Weather Condition"),  # Changed from 天气状况
                            P(f"{current['weather'][0]['description']}"),
                            cls="info-item"
                        ),
                        Div(
                            H3("Location"),  # Changed from 地理位置
                            P(f"Longitude: {current['coord']['lon']}°"),  # Changed from 经度
                            P(f"Latitude: {current['coord']['lat']}°"),   # Changed from 纬度
                            cls="info-item"
                        ),
                        Div(
                            H3("Humidity"),  # Changed from 湿度
                            P(f"{current['main']['humidity']}%"),
                            cls="info-item"
                        ),
                        Div(
                            H3("Wind Speed"),  # Changed from 风速
                            P(f"{current['wind']['speed']} m/s"),
                            cls="info-item"
                        ),
                        Div(
                            H3("Air Pressure"),  # Changed from 气压
                            P(f"{current['main']['pressure']} hPa"),
                            cls="info-item"
                        ),
                        cls="weather-info"
                    ),
                    cls="card-content"
                ),
                cls="info-card"
            )
            
            # 2. Get weather forecast
            forecast_resp = await client.get(
                f"http://api.openweathermap.org/data/2.5/forecast?q={current_city}&appid={api_key}&units=metric&lang=en"
            )
            forecast = forecast_resp.json()
            
            # 3. Get air quality
            lat, lon = current['coord']['lat'], current['coord']['lon']
            air_resp = await client.get(
                f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            )
            air = air_resp.json()
            
            # Air quality card
            air_data = air['list'][0]
            aqi_levels = {
                1: "Excellent",   # Changed from 优
                2: "Good",        # Changed from 良
                3: "Moderate",    # Changed from 轻度污染
                4: "Poor",        # Changed from 中度污染
                5: "Very Poor"    # Changed from 重度污染
            }
            
            air_card = Div(
                Div(
                    H2(f"{current_city} · Air Quality"),  # Changed from 空气质量
                    cls="card-header"
                ),
                Div(
                    Div(
                        Div(
                            H3("AQI Index"),  # Changed from AQI指数
                            P(f"{air_data['main']['aqi']} - {aqi_levels.get(air_data['main']['aqi'], 'Unknown')}", 
                              cls="main-temp"),
                            cls="info-item"
                        ),
                        Div(
                            H3("PM2.5"),
                            P(f"{air_data['components']['pm2_5']:.1f}μg/m³"),
                            cls="info-item"
                        ),
                        Div(
                            H3("PM10"),
                            P(f"{air_data['components']['pm10']:.1f}μg/m³"),
                            cls="info-item"
                        ),
                        Div(
                            H3("CO"),
                            P(f"{air_data['components']['co']:.1f}μg/m³"),
                            cls="info-item"
                        ),
                        Div(
                            H3("NO2"),
                            P(f"{air_data['components']['no2']:.1f}μg/m³"),
                            cls="info-item"
                        ),
                        Div(
                            H3("O3"),
                            P(f"{air_data['components']['o3']:.1f}μg/m³"),
                            cls="info-item"
                        ),
                        cls="weather-info"
                    ),
                    cls="card-content"
                ),
                cls="info-card"
            )
            
            # Get different forecast data according to time range
            forecast_data = forecast['list'][:8] if range == '24h' else forecast['list'][::8][:7]
            forecast_temps = [item['main']['temp'] for item in forecast_data]
            
            if range == '24h':
                forecast_times = [datetime.fromtimestamp(item['dt']).strftime('%H:%M') 
                                 for item in forecast_data]
            else:
                forecast_times = [datetime.fromtimestamp(item['dt']).strftime('%m-%d') 
                                 for item in forecast_data]
            
            # According to user settings, convert temperature unit
            if temp_unit == 'F':
                forecast_temps = [temp * 9/5 + 32 for temp in forecast_temps]
            
            # Create four charts
            charts_container = Div(
                # Temperature trend chart
                Div(
                    H3("Temperature Trend", cls="chart-title"),
                    Canvas(id="tempChart", cls="trend-chart"),
                    Script(f"""
                        new Chart(document.getElementById('tempChart'), {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(forecast_times)},
                                datasets: [{{
                                    label: 'Temperature',
                                    data: {json.dumps(forecast_temps)},
                                    borderColor: '#3b82f6',
                                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                    tension: 0.4,
                                    fill: true,
                                    pointRadius: 4,
                                    pointHoverRadius: 6
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                interaction: {{
                                    mode: 'index',
                                    intersect: false
                                }},
                                plugins: {{
                                    tooltip: {{
                                        enabled: true,
                                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                        titleColor: 'white',
                                        bodyColor: 'white',
                                        padding: 10,
                                        displayColors: false
                                    }},
                                    legend: {{ display: false }}
                                }},
                                scales: {{
                                    y: {{
                                        title: {{
                                            display: true,
                                            text: 'Temperature ({unit})'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    """),
                    cls="chart-wrapper"
                ),
                
                # Humidity trend chart
                Div(
                    H3("Humidity Trend", cls="chart-title"),
                    Canvas(id="humidityChart", cls="trend-chart"),
                    Script(f"""
                        new Chart(document.getElementById('humidityChart'), {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(forecast_times)},
                                datasets: [{{
                                    label: 'Humidity',
                                    data: {json.dumps([item['main']['humidity'] for item in forecast['list'][:8]])},
                                    borderColor: '#10b981',
                                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                    tension: 0.4,
                                    fill: true,
                                    pointRadius: 4,
                                    pointHoverRadius: 6
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                interaction: {{
                                    mode: 'index',
                                    intersect: false
                                }},
                                plugins: {{
                                    tooltip: {{
                                        enabled: true,
                                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                        titleColor: 'white',
                                        bodyColor: 'white',
                                        padding: 10,
                                        displayColors: false
                                    }},
                                    legend: {{ display: false }}
                                }},
                                scales: {{
                                    y: {{
                                        title: {{
                                            display: true,
                                            text: 'Humidity (%)'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    """),
                    cls="chart-wrapper"
                ),
                
                # Wind speed trend chart
                Div(
                    H3("Wind Speed Trend", cls="chart-title"),
                    Canvas(id="windChart", cls="trend-chart"),
                    Script(f"""
                        new Chart(document.getElementById('windChart'), {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(forecast_times)},
                                datasets: [{{
                                    label: 'Wind Speed',
                                    data: {json.dumps([item['wind']['speed'] for item in forecast['list'][:8]])},
                                    borderColor: '#f59e0b',
                                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                                    tension: 0.4,
                                    fill: true,
                                    pointRadius: 4,
                                    pointHoverRadius: 6
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                interaction: {{
                                    mode: 'index',
                                    intersect: false
                                }},
                                plugins: {{
                                    tooltip: {{
                                        enabled: true,
                                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                        titleColor: 'white',
                                        bodyColor: 'white',
                                        padding: 10,
                                        displayColors: false
                                    }},
                                    legend: {{ display: false }}
                                }},
                                scales: {{
                                    y: {{
                                        title: {{
                                            display: true,
                                            text: 'Wind Speed (m/s)'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    """),
                    cls="chart-wrapper"
                ),
                
                # Air pressure trend chart
                Div(
                    H3("Air Pressure Trend", cls="chart-title"),
                    Canvas(id="pressureChart", cls="trend-chart"),
                    Script(f"""
                        new Chart(document.getElementById('pressureChart'), {{
                            type: 'line',
                            data: {{
                                labels: {json.dumps(forecast_times)},
                                datasets: [{{
                                    label: 'Air Pressure',
                                    data: {json.dumps([item['main']['pressure'] for item in forecast['list'][:8]])},
                                    borderColor: '#8b5cf6',
                                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                                    tension: 0.4,
                                    fill: true,
                                    pointRadius: 4,
                                    pointHoverRadius: 6
                                }}]
                            }},
                            options: {{
                                responsive: true,
                                interaction: {{
                                    mode: 'index',
                                    intersect: false
                                }},
                                plugins: {{
                                    tooltip: {{
                                        enabled: true,
                                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                                        titleColor: 'white',
                                        bodyColor: 'white',
                                        padding: 10,
                                        displayColors: false
                                    }},
                                    legend: {{ display: false }}
                                }},
                                scales: {{
                                    y: {{
                                        title: {{
                                            display: true,
                                            text: 'Air Pressure (hPa)'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    """),
                    cls="chart-wrapper"
                ),
                cls="charts-container"
            )
            
            # 24-hour forecast card
            forecast_card = Card(
                H2("24-hour Forecast" if range == '24h' else "5-day Forecast"),
                Div(
                    *[Div(
                        H4(time),
                        P(f"{temp:.1f}{unit}"),
                        P(item['weather'][0]['description']),
                        P(f"Precipitation Probability: {int(item.get('pop', 0) * 100)}%"),
                        P(f"Humidity: {item['main']['humidity']}%"),
                        P(f"Wind Speed: {item['wind']['speed']}m/s"),
                        cls="forecast-item"
                    ) for item, time, temp in zip(
                        forecast_data,
                        forecast_times,
                        forecast_temps
                    )],
                    cls="forecast-grid"
                )
            )

            # Modify dashboard page, add weather analysis card
            weather_analysis = analyze_weather(forecast_data, temp_unit)

            analysis_card = Div(
                Div(H2("Weather Analysis"), cls="analysis-header"),
                Div(
                    Div(
                        # Temperature analysis part
                        Div(
                            H3("Temperature Analysis"),
                            Div(
                                Div(
                                    P("🌡️", cls="stat-icon"),
                                    Div(
                                        H4("Temperature Trend"),
                                        P(weather_analysis['temp_trend']),
                                        cls="stat-info"
                                    ),
                                    cls="analysis-stat"
                                ),
                                Div(
                                    P("📊", cls="stat-icon"),
                                    Div(
                                        H4("Temperature Difference"),
                                        P(f"{weather_analysis['temp_diff']:.1f}{unit}"),
                                        cls="stat-info"
                                    ),
                                    cls="analysis-stat"
                                ),
                            ),
                            Canvas(id="tempTrendChart", cls="analysis-chart"),
                            Script(f"""
                                new Chart(document.getElementById('tempTrendChart'), {{
                                    type: 'line',
                                    data: {{
                                        labels: {json.dumps(forecast_times)},
                                        datasets: [{{
                                            label: 'Temperature Change',
                                            data: {json.dumps(forecast_temps)},
                                            borderColor: '#3b82f6',
                                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                            fill: true,
                                            tension: 0.4
                                        }}]
                                    }},
                                    options: {{
                                        responsive: true,
                                        plugins: {{
                                            legend: {{ display: false }}
                                        }},
                                        scales: {{
                                            y: {{
                                                title: {{
                                                    display: true,
                                                    text: `Temperature (${unit})`
                                                }}
                                            }}
                                        }}
                                    }}
                                }});
                            """),
                            cls="analysis-item"
                        ),
                        
                        # Comfort level analysis part
                        Div(
                            H3("Comfort Level Analysis"),
                            Canvas(id="comfortChart", cls="analysis-chart"),
                            Script(f"""
                                new Chart(document.getElementById('comfortChart'), {{
                                    type: 'bar',
                                    data: {{
                                        labels: {json.dumps(forecast_times)},
                                        datasets: [{{
                                            label: 'Comfort Index',
                                            data: {json.dumps([
                                                0.5 * temp + 0.3 * hum 
                                                for temp, hum in zip(
                                                    [item['main']['temp'] for item in forecast_data],
                                                    [item['main']['humidity'] for item in forecast_data]
                                                )
                                            ])},
                                            backgroundColor: 'rgba(16, 185, 129, 0.7)',
                                            borderRadius: 6
                                        }}]
                                    }},
                                    options: {{
                                        responsive: true,
                                        plugins: {{
                                            legend: {{ display: false }}
                                        }},
                                        scales: {{
                                            y: {{
                                                beginAtZero: true,
                                                title: {{
                                                    display: true,
                                                    text: 'Comfort Index'
                                                }}
                                            }}
                                        }}
                                    }}
                                }});
                            """),
                            Div(
                                *[Div(
                                    P(time, cls="comfort-time"),
                                    P(get_comfort_emoji(level), cls="comfort-emoji"),
                                    P(level, cls="comfort-level"),
                                    cls="comfort-point"
                                ) for time, level in zip(forecast_times, weather_analysis['comfort_levels'])],
                                cls="comfort-timeline"
                            ),
                            cls="analysis-item"
                        ),
                        cls="analysis-grid"
                    ),
                    cls="analysis-content"
                ),
                cls="analysis-container"
            )

    except Exception as e:
        print(f"Weather API error: {e}")
        return Titled("Weather Dashboard",
            Main(
                Div(A('Logout', href='/logout'), style='text-align: right'),
                H1(f"Welcome back, {auth}!"),
                Div(
                    A("Weather Information", href="/dashboard?tab=weather", 
                      cls=f"nav-tab {'active' if tab == 'weather' else ''}"),
                    A("Personal Settings", href="/dashboard?tab=settings",
                      cls=f"nav-tab {'active' if tab == 'settings' else ''}"),
                    cls="nav-tabs"
                ),
                search_form,
                Card(
                    H2("Failed to Get Weather Information"),
                    P("Sorry, unable to get weather information temporarily."),
                    P(f"Error Information: {str(e)}")
                ),
                cls="container dashboard-container"
            )
        )

    # Set form
    settings_form = Form(
        H2("Personal Settings"),
        Div(
            Input(id='city', name='city', value=current_city, required=True),
            label="City",
            cls='input-group'
        ),
        Div(
            P("Temperature Unit:"),
            Div(
                Label(
                    Input(type='radio', name='temp_unit', value='C', 
                          checked=(temp_unit == 'C')),
                    "Celsius (°C)"
                ),
                Label(
                    Input(type='radio', name='temp_unit', value='F',
                          checked=(temp_unit == 'F')),
                    "Fahrenheit (°F)"
                ),
                cls="radio-group"
            ),
            cls='input-group'
        ),
        Button("Save Settings", cls="save-btn"),
        action='/update_settings',
        method='post',
        cls='settings-form'
    )

    # Add time range selector to dashboard page
    time_range_selector = Div(
        Script("""
            function switchTimeRange(range) {
                const buttons = document.querySelectorAll('.time-btn');
                buttons.forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                
                // Get city parameter from current URL
                const urlParams = new URLSearchParams(window.location.search);
                const currentCity = urlParams.get('city');
                
                // Build new URL, keep city parameter
                let newUrl = `/dashboard?range=${range}`;
                if (currentCity) {
                    newUrl += `&city=${currentCity}`;
                }
                
                // Update chart data
                window.location.href = newUrl;
            }
        """),
        Button("24-hour Forecast", 
               onclick="switchTimeRange('24h')",
               cls=f"time-btn {'active' if range == '24h' else ''}"),
        Button("5-day Forecast",
               onclick="switchTimeRange('7d')",
               cls=f"time-btn {'active' if range == '7d' else ''}"),
        cls="time-range-selector"
    )

    return Titled("",
        Main(
            H1("Weather Dashboard", cls="page-title"),  # Add centered title
            Div(
                H1(f"Welcome back, {auth}!"),
                Div(
                    A('Settings', href='/settings', cls="header-btn settings-btn"),
                    A('Logout', href='/logout', cls="header-btn logout-btn"),
                    cls="header-actions"
                ),
                cls="dashboard-header"
            ),
            search_form,
            Div(current_card, air_card, cls="weather-overview"),
            time_range_selector,  # Add time range selector
            charts_container,
            analysis_card,  # Add analysis card
            forecast_card,
            cls="container"
        )
    )

# Logout
@rt("/logout")
def get(sess):
    if 'auth' in sess:
        del sess['auth']
    return login_redir

# Home page redirect to login
@rt("/")
def get(auth=None):
    if auth:
        return RedirectResponse('/dashboard')
    return RedirectResponse('/login')

# Add search route
@rt("/dashboard/search")
async def post(auth, search_city: str):
    return RedirectResponse(f'/dashboard?tab=weather&city={search_city}', status_code=303)

# Add settings page route
@rt("/settings")
def get(auth):
    users = load_users()
    user = users[auth]
    
    return Titled("Settings",
        Main(
            Div(
                H1(f"Welcome back, {auth}!"),
                Div(
                    A('Back to Dashboard', href='/dashboard', cls="header-btn settings-btn"),
                    A('Logout', href='/logout', cls="header-btn logout-btn"),
                    cls="header-actions"
                ),
                cls="dashboard-header"
            ),
            Card(
                Form(
                    H2("Personal Settings"),
                    Div(
                        Input(id='city', name='city', value=user.get('city', ''), required=True),
                        label="Default City",
                        cls='input-group'
                    ),
                    Div(
                        P("Temperature Unit:"),
                        Div(
                            Label(
                                Input(type='radio', name='temp_unit', value='C', 
                                      checked=(user.get('temp_unit', 'C') == 'C')),
                                "Celsius (°C)"
                            ),
                            Label(
                                Input(type='radio', name='temp_unit', value='F',
                                      checked=(user.get('temp_unit', 'F') == 'F')),
                                "Fahrenheit (°F)"
                            ),
                            cls="radio-group"
                        ),
                        cls='input-group'
                    ),
                    Button("Save Settings", cls="save-btn"),
                    action='/update_settings',
                    method='post',
                    cls='settings-form'
                )
            ),
            cls="container"
        )
    )

# Add settings update route
@rt("/update_settings")
async def post(auth, city: str, temp_unit: str):
    users = load_users()
    users[auth]['city'] = city
    users[auth]['temp_unit'] = temp_unit
    save_users(users)
    return RedirectResponse('/dashboard', status_code=303)

# Modify comfort level display in analysis card
def get_comfort_emoji(level: str) -> str:
    """Return corresponding emoji based on comfort level"""
    emoji_map = {
        "Comfortable": "😊",      # Smiling emoji
        "Mild & Dry": "😌",       # Relaxed emoji
        "Mild & Humid": "😅",      # Sweating emoji
        "Cool & Comfortable": "🙂",   # Slightly smiling
        "Cool & Humid": "😕",       # Slightly uncomfortable
        "Cold": "🥶",       # Cold emoji
        "Warm": "😎",       # Sunglasses emoji
        "Warm & Humid": "😓",       # Sweating emoji
        "Hot": "🥵",       # Hot emoji
        "Hot & Humid": "😰",       # Anxious sweating emoji
        "Extremely Hot": "🔥"        # Flame emoji
    }
    return emoji_map.get(level, "😐")  # Default return neutral emoji

serve()