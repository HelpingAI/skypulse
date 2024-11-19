import asyncio
from datetime import datetime
from skypulse import SkyPulse, UnitPreferences

def format_time(time_str):
    # Convert 12-hour format to 24-hour format
    try:
        time = datetime.strptime(time_str, "%I:%M %p")
        return time.strftime("%H:%M")
    except:
        return time_str

def format_temp(temp):
    return f"{temp}°C"

async def test_features():
    # Test with both j1 and j2 formats
    for format in ["j1", "j2"]:
        print(f"\n🌟 Testing with format: {format}")
        print("=" * 50)
        
        async with SkyPulse(async_mode=True, format=format) as client:
            # Set preferred units
            client.set_units(UnitPreferences(
                temperature="C",
                wind_speed="kmh",
                pressure="mb",
                precipitation="mm",
                distance="km"
            ))
            
            # Test locations
            cities = ["Mumbai", "London", "New York"]
            
            # 1. Get current weather
            for city in cities:
                current = await client.get_current_weather_async(city)
                print(f"\n📍 Current Weather in {city}")
                print("=" * 40)
                print(f"🌡️  Temperature: {format_temp(current.temp_C)} ({current.temp_F}°F)")
                print(f"🌡️  Feels Like: {format_temp(current.FeelsLikeC)} ({current.FeelsLikeF}°F)")
                print(f"☁️  Condition: {current.weatherDesc[0].value}")
                print(f"💨 Wind: {current.windspeedKmph} km/h {current.winddir16Point}")
                print(f"💧 Humidity: {current.humidity}%")
                print(f"⬇️  Pressure: {current.pressure} mb")
                print(f"☁️  Cloud Cover: {current.cloudcover}%")
                print(f"👁️  Visibility: {current.visibility} km")
                print(f"☀️  UV Index: {current.uvIndex}")
                print(f"🕒 Local Time: {current.localObsDateTime}")
            
            # 2. Get location details
            for city in cities:
                location = await client.get_location_info_async(city)
                print(f"\n📌 Location Details for {city}")
                print("=" * 40)
                print(f"City: {location.areaName[0].value}")
                print(f"Country: {location.country[0].value}")
                print(f"Region: {location.region[0].value}")
                print(f"Latitude: {location.latitude}")
                print(f"Longitude: {location.longitude}")
                print(f"Population: {location.population}")
            
            # 3. Get forecast
            for city in cities:
                forecast = await client.get_forecast_async(city)
                print(f"\n🔮 Weather Forecast for {city}")
                print("=" * 40)
                for day in forecast:
                    print(f"\nDate: {day.date}")
                    print(f"Max Temperature: {format_temp(day.maxtempC)} ({day.maxtempF}°F)")
                    print(f"Min Temperature: {format_temp(day.mintempC)} ({day.mintempF}°F)")
                    print(f"Average Temperature: {format_temp(day.avgtempC)} ({day.avgtempF}°F)")
                    print(f"Total Snow: {day.totalSnow_cm} cm")
                    print(f"Sun Hours: {day.sunHour}")
                    print(f"UV Index: {day.uvIndex}")
                    
                    astronomy = day.astronomy[0]
                    print("\nAstronomy:")
                    print(f"Sunrise: {format_time(astronomy.sunrise)}")
                    print(f"Sunset: {format_time(astronomy.sunset)}")
                    print(f"Moonrise: {format_time(astronomy.moonrise)}")
                    print(f"Moonset: {format_time(astronomy.moonset)}")
                    print(f"Moon Phase: {astronomy.moon_phase}")
                    print(f"Moon Illumination: {astronomy.moon_illumination}%")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_features())