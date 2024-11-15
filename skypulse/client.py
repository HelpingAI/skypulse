"""SkyPulse client implementation."""

import asyncio
import aiohttp
import requests
from typing import Dict, Any, Optional, Union
from contextlib import asynccontextmanager

from .version import __version__
from .models import Weather, Forecast, Location

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

    DEFAULT_API_URL = "https://weather-omega-taupe.vercel.app/api/weather"
    USER_AGENT = f"SkyPulse-Python/{__version__}"

    def __init__(self, api_url: Optional[str] = None, async_mode: bool = False):
        """Initialize SkyPulse client.

        Args:
            api_url: Base URL for the SkyPulse API. Defaults to the public endpoint.
            async_mode: Whether to use async client. Defaults to False.
        """
        self.base_url = api_url or self.DEFAULT_API_URL
        self.async_mode = async_mode
        
        # Sync client
        if not async_mode:
            self.session = requests.Session()
            self.session.headers.update({"User-Agent": self.USER_AGENT})
        
        # Async client
        self._async_session = None
        self._headers = {"User-Agent": self.USER_AGENT}

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

    def _make_request(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Make synchronous HTTP request to SkyPulse API.

        Args:
            location: Location name or coordinates
            format: Response format (j1 or j2)

        Returns:
            API response data

        Raises:
            LocationError: If location is invalid
            APIError: If API request fails
        """
        params = {
            "location": location,
            "format": format
        }

        try:
            response = self.session.get(self.base_url, params=params)
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

    async def _make_request_async(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Make asynchronous HTTP request to SkyPulse API.

        Args:
            location: Location name or coordinates
            format: Response format (j1 or j2)

        Returns:
            API response data

        Raises:
            LocationError: If location is invalid
            APIError: If API request fails
        """
        if self._async_session is None:
            self._async_session = aiohttp.ClientSession(headers=self._headers)

        params = {
            "location": location,
            "format": format
        }

        try:
            async with self._async_session.get(self.base_url, params=params) as response:
                if response.status == 404:
                    raise LocationError(f"Invalid location: {location}")
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            raise APIError(f"API request failed: {e}")
        except aiohttp.ClientError as e:
            raise APIError(f"Request failed: {e}")
        except ValueError as e:
            raise APIError(f"Invalid JSON response: {e}")

    def get_current(self, location: str, format: str = "j1") -> Weather:
        """Get current weather for a location (synchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Current weather data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no weather data available
        """
        if self.async_mode:
            raise RuntimeError("Use get_current_async for async mode")
            
        data = self._make_request(location, format=format)
        if not data.get("current"):
            raise APIError("No current weather data available")
        return Weather.from_data(data["current"], format=format)

    async def get_current_async(self, location: str, format: str = "j1") -> Weather:
        """Get current weather for a location (asynchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Current weather data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no weather data available
        """
        if not self.async_mode:
            raise RuntimeError("Use get_current for sync mode")
            
        data = await self._make_request_async(location, format=format)
        if not data.get("current"):
            raise APIError("No current weather data available")
        return Weather.from_data(data["current"], format=format)

    def get_forecast(self, location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location (synchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Weather forecast data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no forecast data available
        """
        if self.async_mode:
            raise RuntimeError("Use get_forecast_async for async mode")
            
        data = self._make_request(location, format=format)
        if not data.get("forecast"):
            raise APIError("No forecast data available")
        return Forecast.from_data(data["forecast"], format=format)

    async def get_forecast_async(self, location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location (asynchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Weather forecast data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no forecast data available
        """
        if not self.async_mode:
            raise RuntimeError("Use get_forecast for sync mode")
            
        data = await self._make_request_async(location, format=format)
        if not data.get("forecast"):
            raise APIError("No forecast data available")
        return Forecast.from_data(data["forecast"], format=format)

    def get_all(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Get both current weather and forecast for a location (synchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Dictionary containing:
                - current: Current weather data
                - forecast: Weather forecast data
                - location: Location data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no weather data available
        """
        if self.async_mode:
            raise RuntimeError("Use get_all_async for async mode")
            
        data = self._make_request(location, format=format)
        if not data.get("current") or not data.get("forecast"):
            raise APIError("Missing weather data in response")

        return {
            "current": Weather.from_data(data["current"], format=format),
            "forecast": Forecast.from_data(data["forecast"], format=format),
            "location": Location.from_data(data.get("location", {}), format=format),
            "request": data.get("request", {})
        }

    async def get_all_async(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Get both current weather and forecast for a location (asynchronous).

        Args:
            location: Location name or coordinates
            format: API format version (j1 or j2)

        Returns:
            Dictionary containing:
                - current: Current weather data
                - forecast: Weather forecast data
                - location: Location data

        Raises:
            APIError: If request fails or invalid response
            LocationError: If location not found
            ValueError: If no weather data available
        """
        if not self.async_mode:
            raise RuntimeError("Use get_all for sync mode")
            
        data = await self._make_request_async(location, format=format)
        if not data.get("current") or not data.get("forecast"):
            raise APIError("Missing weather data in response")

        return {
            "current": Weather.from_data(data["current"], format=format),
            "forecast": Forecast.from_data(data["forecast"], format=format),
            "location": Location.from_data(data.get("location", {}), format=format),
            "request": data.get("request", {})
        }

    def __str__(self) -> str:
        """Return string representation of SkyPulse client."""
        mode = "async" if self.async_mode else "sync"
        return f"SkyPulse(api_url='{self.base_url}', mode='{mode}')"
