"""SkyPulse client implementation."""

import requests
from typing import Dict, Any, Optional

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
    """Main SkyPulse client."""

    DEFAULT_API_URL = "https://weather-omega-taupe.vercel.app/api/weather"
    USER_AGENT = f"SkyPulse-Python/{__version__}"

    def __init__(self, api_url: Optional[str] = None):
        """Initialize SkyPulse client.

        Args:
            api_url: Base URL for the SkyPulse API. Defaults to the public endpoint.
        """
        self.base_url = api_url or self.DEFAULT_API_URL
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})

    def _make_request(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Make HTTP request to SkyPulse API.

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

    def get_current(self, location: str, format: str = "j1") -> Weather:
        """Get current weather for a location.

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
        data = self._make_request(location, format=format)
        if not data.get("current"):
            raise APIError("No current weather data available")
        return Weather.from_data(data["current"], format=format)

    def get_forecast(self, location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location.

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
        data = self._make_request(location, format=format)
        if not data.get("forecast"):
            raise APIError("No forecast data available")
        return Forecast.from_data(data["forecast"], format=format)

    def get_all(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Get both current weather and forecast for a location.

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
        data = self._make_request(location, format=format)

        if not data.get("current") or not data.get("forecast"):
            raise APIError("Missing weather data in response")

        result = {
            "current": Weather.from_data(data["current"], format=format),
            "forecast": Forecast.from_data(data["forecast"], format=format),
            "location": Location.from_data(data.get("location", {}), format=format)
        }

        return result

    def __str__(self) -> str:
        """Return string representation of SkyPulse client."""
        return f"SkyPulse(api_url='{self.base_url}')"
