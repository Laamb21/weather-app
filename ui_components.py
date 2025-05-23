import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Callable, Dict, Optional

from config import (
    WINDOW_WIDTH, 
    WINDOW_HEIGHT, 
    WINDOW_TITLE, 
    REFRESH_INTERVAL,
    ERROR_NO_DATA
)

class WeatherCard(ttk.Frame):
    """A card widget displaying weather information for a city"""
    def __init__(self, parent, city: str):
        super().__init__(parent)
        self.city = city
        
        # Configure card style
        self.configure(relief="raised", padding=10)
        
        # City name
        self.city_label = ttk.Label(self, text=city, font=("Arial", 14, "bold"))
        self.city_label.pack(anchor="w")
        
        # Temperature
        self.temp_label = ttk.Label(self, text="--°F", font=("Arial", 24))
        self.temp_label.pack()
        
        # Condition
        self.condition_label = ttk.Label(self, text="Loading...")
        self.condition_label.pack()
        
        # Forecast
        self.forecast_label = ttk.Label(self, text="", wraplength=200)
        self.forecast_label.pack(pady=(10, 0))

    def update_weather(self, temp: Optional[int], condition: str, forecast: str):
        """Update the weather information displayed on the card"""
        if temp is not None:
            self.temp_label.config(text=f"{temp}°F")
        self.condition_label.config(text=condition)
        self.forecast_label.config(text=forecast)

class WeatherDashboard(tk.Tk):
    """Main weather dashboard window"""
    def __init__(self, get_cities_func: Callable, get_weather_func: Callable):
        super().__init__()
        
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Store callbacks
        self.get_cities = get_cities_func
        self.get_weather = get_weather_func
        
        # Create main container with scrollbar
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create canvas for scrolling
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar components
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Weather cards for each city
        self.weather_cards: Dict[str, WeatherCard] = {}
        self.initialize_weather_cards()
        
        # Start weather update loop
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()

    def initialize_weather_cards(self):
        """Create weather cards for all cities"""
        cities = self.get_cities()
        
        # Create grid of weather cards
        row = 0
        col = 0
        for city in cities:
            card = WeatherCard(self.scrollable_frame, city)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.weather_cards[city] = card
            
            col += 1
            if col >= 3:  # 3 cards per row
                col = 0
                row += 1

    def update_loop(self):
        """Background loop to update weather data"""
        while True:
            self.update_all_weather()
            time.sleep(REFRESH_INTERVAL * 60)  # Convert minutes to seconds

    def update_all_weather(self):
        """Update weather for all cities"""
        for city, card in self.weather_cards.items():
            try:
                weather_data = self.get_weather(city)
                if weather_data:
                    card.update_weather(
                        temp=weather_data.get('temperature'),
                        condition=weather_data.get('condition', 'Unknown'),
                        forecast=weather_data.get('forecast', 'No forecast available')
                    )
            except Exception as e:
                card.update_weather(None, ERROR_NO_DATA, str(e))
