"""Style Definition Module

This module defines application stylesheets.

Main features:
    - Base style definitions
    - Dashboard style configuration
    - Responsive layout styles
    - Theme style definitions

Constants:
    custom_style (str): Base custom styles including root variables and body styles
    dashboard_style (str): Dashboard page styles including layout and components
"""

# Base styles
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

# Dashboard styles
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
"""

# Style utility functions
def get_theme_styles(theme: str) -> str:
    """Get styles for specified theme
    
    Args:
        theme (str): Theme name ('light' or 'dark')
    
    Returns:
        str: Theme-specific CSS styles
    """
    pass 