# city_data.py

'''
Major US cities with coordinates for weather 
'''

import json
import os

# Cache for loaded city data
_cities_cache = None

def _load_cities():
    ''' Load cities from JSON file '''
    global _cities_cache

    if _cities_cache is not None:
        return _cities_cache
    
    try:
        # Look for cities.json in the same directory as script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, 'cities.json')

        with open(json_path, 'r', encoding='utf-8') as file:
            cities_data = json.load(file)

        # Cache loaded data
        _cities_cache = cities_data['cities']  # Access the 'cities' key from the JSON
        return _cities_cache
    
    except FileNotFoundError:
        print("Error: cities.json file not found. Please ensure it exists in the same directory.")
        return [] 
    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in cities.json file: {e}")
        return []
    
    except Exception as e:
        print(f"Error loading cities.json: {e}")
        return []
    
def get_city_list():
    ''' Return formatted list of cities for UI display '''
    cities = _load_cities()
    if not cities:
        return []
    
    return sorted(city['city'] for city in cities)

def get_city_coordinates(city_name):
    ''' Get coordinates for a specific city '''
    cities = _load_cities()
    for city in cities:
        if city['city'] == city_name:
            return float(city['latitude']), float(city['longitude'])
    return None