"""SkyPulse client implementation."""

import aiohttp
import requests
from typing import Dict, Any, Optional, List
from contextlib import asynccontextmanager
import asyncio

from .version import __version__
from .models import WttrResponse, CurrentCondition, Weather, NearestArea, UnitPreferences

class SkyPulseError(Exception):
    """Base exception for SkyPulse errors."""
    pass

class APIError(SkyPulseError):
    """API related errors."""
    pass

class LocationError(SkyPulseError):
    """Location related errors."""
    pass

class SkyPulse:
    """Main SkyPulse client with both sync and async support."""

    DEFAULT_API_URL = "https://wttr.in"
    USER_AGENT = f"SkyPulse-Python/{__version__}"

    def __init__(self, api_url: Optional[str] = None, async_mode: bool = False, format: str = "j1"):
        """Initialize SkyPulse client.

        Args:
            api_url: Base URL for the SkyPulse API. Defaults to the public endpoint.
            async_mode: Whether to use async client. Defaults to False.
            format: API response format, either "j1" or "j2". Defaults to "j1".
        """
        self.base_url = api_url or self.DEFAULT_API_URL
        self.async_mode = async_mode
        self.format = format
        if format not in ["j1", "j2"]:
            raise ValueError("Format must be either 'j1' or 'j2'")
        
        # Sync client
        if not async_mode:
            self.session = requests.Session()
            self.session.headers.update({"User-Agent": self.USER_AGENT})
        
        # Async client
        self._async_session = None
        self._headers = {"User-Agent": self.USER_AGENT}
        self._unit_preferences = None

    async def __aenter__(self):
        """Async context manager entry."""
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession(headers=self._headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._async_session is not None:
            await self._async_session.close()
            self._async_session = None

    def _make_request(self, location: str, **params) -> Dict[str, Any]:
        """Make synchronous HTTP request to SkyPulse API."""
        params.update({
            "format": self.format
        })
        
        url = f"{self.base_url}/{location}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise LocationError(f"Invalid location: {location}")
            raise APIError(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")
        except ValueError as e:
            raise APIError(f"Invalid JSON response: {e}")

    async def _make_request_async(self, location: str, **params) -> Dict[str, Any]:
        """Make asynchronous HTTP request to SkyPulse API."""
        params.update({
            "format": self.format
        })

        if not self._async_session:
            raise APIError("No active async session. Use 'async with' context manager.")

        url = f"{self.base_url}/{location}"
        try:
            async with self._async_session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e.status == 404:
                raise LocationError(f"Invalid location: {location}")
            raise APIError(f"API request failed: {e}")
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {e}")
        except ValueError as e:
            raise APIError(f"Invalid JSON response: {e}")

    def set_units(self, preferences: UnitPreferences) -> None:
        """Set unit preferences for weather data.
        
        Args:
            preferences: UnitPreferences object with desired units
        """
        self._unit_preferences = preferences

    def get_weather(self, location: str) -> WttrResponse:
        """Get weather data for a location.

        Args:
            location: Location to get weather for.

        Returns:
            WttrResponse object containing weather data.

        Raises:
            APIError: If the API request fails.
        """
        if self.async_mode:
            raise APIError("Use get_weather_async for async mode")
        
        data = self._make_request(location)
        return WttrResponse.from_dict(data)

    async def get_weather_async(self, location: str) -> WttrResponse:
        """Get weather data for a location asynchronously.

        Args:
            location: Location to get weather for.

        Returns:
            WttrResponse object containing weather data.

        Raises:
            APIError: If the API request fails.
        """
        if not self.async_mode:
            raise APIError("Client is not in async mode")

        data = await self._make_request_async(location)
        return WttrResponse.from_dict(data)

    def get_current_weather(self, location: str) -> CurrentCondition:
        """Get current weather conditions for a location.

        Args:
            location: Location to get weather for.

        Returns:
            CurrentCondition object containing current weather data.
        """
        response = self.get_weather(location)
        if not response.current_condition:
            raise APIError("No current weather data available")
        return response.current_condition[0]

    async def get_current_weather_async(self, location: str) -> CurrentCondition:
        """Get current weather conditions for a location asynchronously.

        Args:
            location: Location to get weather for.

        Returns:
            CurrentCondition object containing current weather data.
        """
        response = await self.get_weather_async(location)
        if not response.current_condition:
            raise APIError("No current weather data available")
        return response.current_condition[0]

    def get_forecast(self, location: str) -> List[Weather]:
        """Get weather forecast for a location.

        Args:
            location: Location to get weather for.

        Returns:
            List of Weather objects containing forecast data.
        """
        response = self.get_weather(location)
        return response.weather

    async def get_forecast_async(self, location: str) -> List[Weather]:
        """Get weather forecast for a location asynchronously.

        Args:
            location: Location to get weather for.

        Returns:
            List of Weather objects containing forecast data.
        """
        response = await self.get_weather_async(location)
        return response.weather

    def get_location_info(self, location: str) -> NearestArea:
        """Get location information.

        Args:
            location: Location to get info for.

        Returns:
            NearestArea object containing location data.
        """
        response = self.get_weather(location)
        if not response.nearest_area:
            raise APIError("No location data available")
        return response.nearest_area[0]

    async def get_location_info_async(self, location: str) -> NearestArea:
        """Get location information asynchronously.

        Args:
            location: Location to get info for.

        Returns:
            NearestArea object containing location data.
        """
        response = await self.get_weather_async(location)
        if not response.nearest_area:
            raise APIError("No location data available")
        return response.nearest_area[0]

    def compare_locations(self, locations: List[str]) -> Dict[str, WttrResponse]:
        """Compare current weather between multiple locations.
        
        Args:
            locations: List of location names or coordinates
        """
        result = {}
        for location in locations:
            result[location] = self.get_weather(location)
        return result

    async def compare_locations_async(self, locations: List[str]) -> Dict[str, WttrResponse]:
        """Compare current weather between multiple locations asynchronously."""
        result = {}
        tasks = [self.get_weather_async(location) for location in locations]
        weather_data = await asyncio.gather(*tasks, return_exceptions=True)
        
        for location, data in zip(locations, weather_data):
            if isinstance(data, Exception):
                result[location] = None
            else:
                result[location] = data
        return result

    def __str__(self) -> str:
        """Return string representation of SkyPulse client."""
        mode = "async" if self.async_mode else "sync"
        return f"SkyPulse(api_url='{self.base_url}', mode='{mode}', format='{self.format}')"
