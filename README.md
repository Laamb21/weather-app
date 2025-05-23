# US Cities Weather Dashboard

A Python-based weather dashboard application that displays real-time weather information for major US cities using the National Weather Service (NWS) API.

## Features

- Real-time weather data for major US cities
- Current temperature and conditions
- Multi-day weather forecasts
- Auto-refreshing weather data (every 10 minutes)
- Clean, modern UI with scrollable city cards
- Error handling and offline support

## Requirements

- Python 3.7+
- Tkinter (usually comes with Python)
- Internet connection for weather data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Laamb21/weather-app.git
cd us-cities-weather-dashboard
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. The dashboard will open showing weather cards for all configured cities
3. Weather data automatically refreshes every 10 minutes
4. Scroll to view all cities if they don't fit on screen

## Configuration

The application can be configured by modifying `config.py`:

- `REFRESH_INTERVAL`: Time between weather updates (in minutes)
- `MAX_FORECAST_DAYS`: Number of days to show in the forecast
- `WINDOW_WIDTH/HEIGHT`: Application window dimensions
- Other API and display settings

## Project Structure

- `main.py` - Application entry point
- `ui_components.py` - Tkinter UI components
- `weather_service.py` - NWS API interaction
- `city_data.py` - City information management
- `config.py` - Application configuration
- `cities.json` - City database with coordinates

## Error Handling

The application handles various error conditions:
- Network connectivity issues
- API timeouts
- Invalid data responses
- Missing city information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Weather data provided by the [National Weather Service API](https://weather-gov.github.io/api/)