# config.py

'''
Configuration settings for weather app
'''

# National Weather Service API Configuration
NWS_BASE_URL = "https://api.weather.gov"
REQUEST_TIMEOUT = 10 # seconds
MAX_RETRIES = 3

# Application settings
REFRESH_INTERVAL = 10 # minutes
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_TITLE = "US CITIES WEATHER APP"

# Display settings
TEMPERATURE_UNIT = "F"
SHOW_DETAILED_FORECAST = True
MAX_FORECAST_DAYS = 7

# Error Messages
ERROR_NO_INTERNET = "Unable to connect to the weather service. Check internet connection."
ERROR_NO_DATA = "Weather data not available for this location."
ERROR_API_TIMEOUT = "Weather service is taking too long to respond."