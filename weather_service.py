import requests
from typing import Dict, Optional, Tuple
import json
from datetime import datetime

from config import (
    ERROR_NO_DATA,
    NWS_BASE_URL,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    ERROR_NO_INTERNET,
    ERROR_API_TIMEOUT,
    MAX_FORECAST_DAYS
)

class WeatherService:
    """Service for fetching weather data from National Weather Service API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': '(US Cities Weather App, your@email.com)',
            'Accept': 'application/json'
        })
        
    def get_weather_data(self, lat: float, lon: float) -> Dict:
        """Get weather data for a specific location"""
        try:
            # Get grid coordinates
            point_url = f"{NWS_BASE_URL}/points/{lat},{lon}"
            point_response = self._make_request(point_url)
            
            if not point_response:
                return self._error_response(ERROR_NO_DATA)
            
            # Get forecast office endpoints
            forecast_url = point_response['properties']['forecast']
            hourly_url = point_response['properties']['forecastHourly']
            
            # Get current conditions and forecast
            forecast_data = self._make_request(forecast_url)
            hourly_data = self._make_request(hourly_url)
            
            if not forecast_data or not hourly_data:
                return self._error_response(ERROR_NO_DATA)
            
            # Process the data
            current_temp = self._get_current_temp(hourly_data)
            current_condition = self._get_current_condition(forecast_data)
            forecast = self._get_forecast_text(forecast_data)
            
            return {
                'temperature': current_temp,
                'condition': current_condition,
                'forecast': forecast,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.ConnectionError:
            return self._error_response(ERROR_NO_INTERNET)
        except requests.exceptions.Timeout:
            return self._error_response(ERROR_API_TIMEOUT)
        except Exception as e:
            return self._error_response(str(e))
    
    def _make_request(self, url: str) -> Optional[Dict]:
        """Make HTTP request with retries"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.json()
            except:
                if attempt == MAX_RETRIES - 1:
                    raise
                continue
        return None
    
    def _get_current_temp(self, hourly_data: Dict) -> int:
        """Extract current temperature from hourly forecast"""
        try:
            current_period = hourly_data['properties']['periods'][0]
            return round(current_period['temperature'])
        except (KeyError, IndexError):
            return None
    
    def _get_current_condition(self, forecast_data: Dict) -> str:
        """Extract current weather condition"""
        try:
            current_period = forecast_data['properties']['periods'][0]
            return current_period['shortForecast']
        except (KeyError, IndexError):
            return "Unknown"
    
    def _get_forecast_text(self, forecast_data: Dict) -> str:
        """Create forecast text from forecast data"""
        try:
            periods = forecast_data['properties']['periods'][:MAX_FORECAST_DAYS * 2]  # 2 periods per day
            forecast_parts = []
            
            for period in periods:
                name = period['name']
                forecast = period['shortForecast']
                temp = period['temperature']
                forecast_parts.append(f"{name}: {temp}°F, {forecast}")
            
            return "\n".join(forecast_parts)
        except (KeyError, IndexError):
            return "Forecast unavailable"
    
    def _error_response(self, message: str) -> Dict:
        """Create error response"""
        return {
            'temperature': None,
            'condition': 'Error',
            'forecast': message,
            'timestamp': datetime.now().isoformat()
        } 