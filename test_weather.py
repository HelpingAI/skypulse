from skypulse import SkyPulse

def test_weather():
    # Initialize client
    client = SkyPulse()
    
    try:
        # Get current weather (basic format)
        print("\nTesting basic format (j1):")
        current = client.get_current("London")
        print(f"Temperature: {current.temperature_c}°C ({current.temperature_f}°F)")
        print(f"Feels like: {current.feels_like_c}°C")
        print(f"Humidity: {current.humidity}%")
        print(f"Wind: {current.wind_speed_kmh} km/h {current.wind_direction}")
        
        # Get detailed weather data (v2 format)
        print("\nTesting extended format (j2):")
        data = client.get_all("London", format="j2")
        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]
        request = data["request"]
        
        print(f"\nLocation: {location.name}, {location.country}")
        print(f"Query: {request.query}")
        print(f"Current: {current.temperature_c}°C, {current.condition.description}")
        
        print("\nForecast:")
        for day in forecast.days:
            print(f"\n{day.date}:")
            print(f"  Temperature: {day.min_temp_c}°C to {day.max_temp_c}°C")
            print(f"  UV Index: {day.uv_index}")
            print(f"  Sun hours: {day.sun_hour}")
            
            astro = day.astronomy
            print(f"  Sunrise: {astro.sunrise}")
            print(f"  Sunset: {astro.sunset}")
            print(f"  Moon phase: {astro.moon_phase}")
            
    except Exception as e:
        print(f"Error: {e}")

    # Test current weather
    current = client.get_current("London")
    assert current.temperature_c is not None
    assert current.temperature_f is not None
    assert current.feels_like_c is not None
    assert current.humidity is not None
    assert current.wind_speed_kmh is not None
    assert current.wind_direction is not None
    
    # Test forecast
    forecast = client.get_forecast("London", days=3)
    assert len(forecast.days) == 3
    for day in forecast.days:
        assert day.date is not None
        assert day.max_temp_c is not None
        assert day.min_temp_c is not None
        assert day.condition is not None
        
        astro = day.astronomy
        assert astro.sunrise is not None
        assert astro.sunset is not None
        assert astro.moon_phase is not None

if __name__ == "__main__":
    test_weather()
