from ui_components import WeatherDashboard
from weather_service import WeatherService
from city_data import get_city_list, get_city_coordinates

def main():
    # Initialize weather service
    weather_service = WeatherService()
    
    def get_weather(city):
        """Get weather data for a city"""
        coordinates = get_city_coordinates(city)
        if coordinates:
            lat, lon = coordinates
            return weather_service.get_weather_data(lat, lon)
        return None
    
    # Create and run dashboard
    dashboard = WeatherDashboard(get_city_list, get_weather)
    dashboard.mainloop()

if __name__ == "__main__":
    main()