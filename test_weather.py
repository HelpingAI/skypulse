import asyncio
from skypulse import SkyPulse

async def get_weather():
    # Initialize async client
    async with SkyPulse(async_mode=True) as client:
        # Get current weather
        current = await client.get_current_async("London")
        print(f"Temperature: {current.temperature_c}°C")

        # Get forecast
        forecast = await client.get_forecast_async("London")
        for day in forecast.days:
            print(f"Date: {day.date}, Max: {day.max_temp_c}°C")

        # Get all weather data
        data = await client.get_all_async("London", format="j2")
        print(f"Location: {data['location'].name}")
        print(f"Current: {data['current'].temperature_c}°C")

# Run async code
asyncio.run(get_weather())