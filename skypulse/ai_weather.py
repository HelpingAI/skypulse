"""Weather analysis with comprehensive AI reporting."""

import os
import sys
import requests
from datetime import datetime, timedelta
from typing import Generator, Dict, Any, Optional
from openai import OpenAI

from skypulse.models import Weather, Forecast, Location, WeatherData
from skypulse.client import SkyPulse

class WeatherAnalyzer:
    """Enhanced weather analysis using OpenAI and SkyPulse."""

    EMOJIS = {
        "sunny": "☀️", "partly_sunny": "🌤️", "cloudy": "☁️",
        "rainy": "🌧️", "stormy": "⛈️", "snowy": "❄️",
        "windy": "💨", "foggy": "🌫️", "hot": "🔥",
        "cold": "🥶", "perfect": "👌", "warning": "⚠️",
        "sunrise": "🌅", "sunset": "🌇", "moon": "🌙",
        "thermometer": "🌡️", "droplet": "💧", "wind": "🌪️",
        "uv": "☀️", "compass": "🧭", "clock": "⏰",
        "calendar": "📅", "location": "📍", "alert": "🚨"
    }

    WEATHER_MOODS = {
        "sunny": ["energetic", "vibrant", "cheerful"],
        "cloudy": ["cozy", "calm", "peaceful"],
        "rainy": ["relaxing", "refreshing", "contemplative"],
        "stormy": ["dramatic", "intense", "powerful"],
        "snowy": ["magical", "serene", "pristine"],
        "perfect": ["delightful", "amazing", "fantastic"]
    }

    def __init__(self, openai_base_url: Optional[str] = None, openai_api_key: Optional[str] = None):
        """Initialize the analyzer with OpenAI and SkyPulse clients."""
        self.openai_api_key = openai_api_key or "dummy_api_key"
        self.openai_client = OpenAI(
            api_key=self.openai_api_key,
            base_url=openai_base_url or "https://chatcfapi.r12.top/v1"
        )
        self.weather_client = SkyPulse(async_mode=False)
        self._ip_location = None

    def _get_ip_location(self) -> str:
        """Get location from IP address."""
        if not self._ip_location:
            response = requests.get('https://ipapi.co/json/')
            data = response.json()
            self._ip_location = f"{data['city']}, {data['country_name']}"
        return self._ip_location

    def _get_weather_mood(self, condition: str, temp: float) -> str:
        """Get the mood/vibe of the weather."""
        condition = condition.lower()
        for weather_type, moods in self.WEATHER_MOODS.items():
            if weather_type in condition:
                return moods[0]
        if temp > 30:
            return "energetic"
        elif temp < 10:
            return "crisp"
        return "perfect"

    def _get_weather_emoji(self, condition: str, temp: float) -> str:
        """Get appropriate emoji for weather condition."""
        condition = condition.lower()
        if "sun" in condition and "cloud" in condition:
            return self.EMOJIS["partly_sunny"]
        elif "sun" in condition or "clear" in condition:
            return self.EMOJIS["sunny"]
        elif "cloud" in condition:
            return self.EMOJIS["cloudy"]
        elif "rain" in condition:
            return self.EMOJIS["rainy"]
        elif "storm" in condition or "thunder" in condition:
            return self.EMOJIS["stormy"]
        elif "snow" in condition:
            return self.EMOJIS["snowy"]
        elif "fog" in condition or "mist" in condition:
            return self.EMOJIS["foggy"]
        elif "wind" in condition:
            return self.EMOJIS["windy"]
        elif temp > 30:
            return self.EMOJIS["hot"]
        elif temp < 10:
            return self.EMOJIS["cold"]
        return self.EMOJIS["perfect"]

    def _format_weather_data(self, weather_data: WeatherData) -> str:
        """Format comprehensive weather data for analysis."""
        current = weather_data.current
        forecast = weather_data.forecast
        location = weather_data.location
        
        # Get weather characteristics
        emoji = self._get_weather_emoji(current.condition.description, current.temperature_c)
        mood = self._get_weather_mood(current.condition.description, current.temperature_c)
        
        # Format current conditions with optional attributes
        current_conditions = [
            f"Hey weather enthusiasts! {self.EMOJIS['location']} Let's dive into the weather vibes at {location.name}, {location.country}!",
            f"\n{self.EMOJIS['clock']} CURRENT CONDITIONS {emoji}",
            f"• Temperature: {self.EMOJIS['thermometer']} {current.temperature_c}°C (feels like {current.feels_like_c}°C)",
            f"• Weather: {emoji} {current.condition.description} - {mood} vibes!",
            f"• Wind: {self.EMOJIS['wind']} {current.wind_speed_kmh} km/h from {current.wind_direction}",
            f"• Humidity: {self.EMOJIS['droplet']} {current.humidity}%"
        ]

        # Add optional current conditions if available
        if hasattr(current, 'uv_index'):
            current_conditions.append(f"• UV Index: {self.EMOJIS['uv']} {current.uv_index}")
        if hasattr(current, 'pressure_mb'):
            current_conditions.append(f"• Pressure: {current.pressure_mb} mb")
        if hasattr(current, 'visibility_km'):
            current_conditions.append(f"• Visibility: {current.visibility_km} km")

        # Join current conditions
        current_data = "\n".join(current_conditions)

        # Format forecast with available data
        forecast_lines = [
            f"\n\n{self.EMOJIS['calendar']} 3-DAY FORECAST",
            f"• Today: {forecast.days[0].min_temp_c}°C to {forecast.days[0].max_temp_c}°C"
        ]

        # Add astronomy data if available
        if hasattr(forecast.days[0], 'astronomy'):
            astronomy = forecast.days[0].astronomy
            if hasattr(astronomy, 'sunrise'):
                forecast_lines.append(f"  - Sunrise: {self.EMOJIS['sunrise']} {astronomy.sunrise}")
            if hasattr(astronomy, 'sunset'):
                forecast_lines.append(f"  - Sunset: {self.EMOJIS['sunset']} {astronomy.sunset}")
            if hasattr(astronomy, 'moon_phase'):
                forecast_lines.append(f"  - Moon Phase: {self.EMOJIS['moon']} {astronomy.moon_phase}")

        # Add remaining forecast days
        if len(forecast.days) > 1:
            forecast_lines.append(f"• Tomorrow: {forecast.days[1].min_temp_c}°C to {forecast.days[1].max_temp_c}°C")
        if len(forecast.days) > 2:
            forecast_lines.append(f"• Day After: {forecast.days[2].min_temp_c}°C to {forecast.days[2].max_temp_c}°C")

        # Join forecast data
        forecast_data = "\n".join(forecast_lines)

        # Format alerts based on available data
        alerts = []
        if hasattr(current, 'uv_index') and current.uv_index > 7:
            alerts.append(f"\n\n{self.EMOJIS['alert']} ALERTS\n• High UV Index! Sun protection recommended!")
        if current.wind_speed_kmh > 50:
            alerts.append(f"\n\n{self.EMOJIS['alert']} ALERTS\n• Strong winds! Take care outdoors!")

        # Combine all sections
        return current_data + forecast_data + "".join(alerts)

    def _get_weather_data(self, location: str) -> WeatherData:
        """Get comprehensive weather data."""
        current = self.weather_client.get_current(location)
        forecast = self.weather_client.get_forecast(location)
        location_info = self.weather_client.get_location(location)
        return WeatherData(current, forecast, location_info)

    def _get_ai_analysis(self, weather_data: WeatherData) -> Generator[str, None, None]:
        """Get streaming AI weather report."""
        prompt = f"""You're a charismatic weather reporter with a Gen-Z vibe! Create an engaging weather report from this data:

{self._format_weather_data(weather_data)}

Your report should include:
1. A catchy intro with the current vibe/mood of the weather
2. The most interesting/important current conditions (temp, feel, notable elements)
3. What to expect in the next 24 hours
4. Fun activity suggestions based on the weather
5. Any relevant weather tips or warnings
6. A creative sign-off that matches the weather mood

Style Guide:
- Be super engaging and conversational
- Use emojis naturally
- Include some weather-related slang or puns
- Keep each point concise but informative
- Add your personality!

Make it feel like a friend giving weather advice!"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You're a trendy weather reporter who makes weather fun and relatable!"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=500,
                stream=True
            )

            for chunk in response:
                if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error generating weather report: {str(e)}"

def print_weather_insights(location: Optional[str] = None):
    """Print weather insights for a location."""
    analyzer = WeatherAnalyzer()
    location = location or analyzer._get_ip_location()
    weather_data = analyzer._get_weather_data(location)
    for text in analyzer._get_ai_analysis(weather_data):
        print(text, end="", flush=True)

def main():
    """Run weather analysis with error handling."""
    try:
        print_weather_insights()
    except KeyboardInterrupt:
        print("\nWeather analysis interrupted.")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
