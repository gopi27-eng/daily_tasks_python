import requests

API_URL = "https://api.mockflights.com/weather/guwahati"

def get_weather_status():
    
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"Error: Unable to fetch weather data status: {response.status_code}.")
            return
        
        data = response.json()
        wind_speed = data["conditions"]["wind"]["speed_knots"]
        visibility = data["conditions"]["visibility_km"]

        print(f"Station: {data['station']}")
        print(f"Timestamp: {data['timestamp']}")
        print(f"Temperature: {data['conditions']['temperature_c']} °C")
        print(f"Wind: {wind_speed} knots, Direction: {data['conditions']['wind']['direction']}")
        print(f"Visibility: {visibility} km")
        print(f"Flight Status: {data['flight_status']}")   
        
        if (wind_speed > 20 or visibility < 5):
            print("Warning: Adverse weather conditions detected. Flight operations may be affected.")
    except Exception as e:
        print(f"Error occurred while fetching weather data: {str(e)}") 