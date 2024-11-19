"""Real-time weather notification system with streaming support."""

import asyncio
import json
from typing import Optional, AsyncGenerator, Dict, Any
from datetime import datetime
import aiohttp
from dataclasses import dataclass

from .client import SkyPulse
from .models import Weather, Location

@dataclass
class WeatherNotification:
    """Compact weather notification format."""
    temperature: float
    condition: str
    location: str
    timestamp: str

    @classmethod
    def from_weather(cls, weather: Weather, location: str) -> 'WeatherNotification':
        """Create notification from weather data."""
        return cls(
            temperature=weather.temperature_c,
            condition=weather.condition.description,
            location=location,
            timestamp=datetime.now().isoformat()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            "temperature": self.temperature,
            "condition": self.condition,
            "location": self.location,
            "timestamp": self.timestamp
        }

class WeatherNotifier:
    """Real-time weather notification system."""

    def __init__(self, update_interval: int = 300):
        """Initialize the notifier.
        
        Args:
            update_interval: Time between updates in seconds (default: 5 minutes)
        """
        self.client = SkyPulse(async_mode=True)
        self.update_interval = update_interval
        self._location: Optional[str] = None
        self._ip_location: Optional[str] = None

    async def _get_ip_location(self) -> str:
        """Get location from IP address."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://ipapi.co/json/') as response:
                data = await response.json()
                return f"{data['city']}, {data['country_name']}"

    async def _get_location(self) -> str:
        """Get current location (user-provided or IP-based)."""
        if self._location:
            return self._location
        if not self._ip_location:
            self._ip_location = await self._get_ip_location()
        return self._ip_location

    def set_location(self, location: str):
        """Set a specific location for weather updates."""
        self._location = location

    async def get_current_notification(self) -> WeatherNotification:
        """Get current weather notification."""
        location = await self._get_location()
        async with self.client:
            weather = await self.client.get_current_async(location)
            return WeatherNotification.from_weather(weather, location)

    async def stream_notifications(self) -> AsyncGenerator[WeatherNotification, None]:
        """Stream weather notifications in real-time."""
        while True:
            try:
                notification = await self.get_current_notification()
                yield notification
                await asyncio.sleep(self.update_interval)
            except Exception as e:
                print(f"Error getting weather update: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying

async def print_weather_updates(notifier: WeatherNotifier):
    """Print weather updates to console."""
    async for notification in notifier.stream_notifications():
        print(f"\r{notification.location}: {notification.temperature}°C, {notification.condition}", end="", flush=True)

# Example usage:
async def main():
    notifier = WeatherNotifier(update_interval=300)  # Update every 5 minutes
    # Optional: Set specific location
    # notifier.set_location("London, UK")
    await print_weather_updates(notifier)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopping weather updates...")
