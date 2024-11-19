"""SkyPulse Weather Data Package."""

from .version import __version__, __prog__
from .client import SkyPulse, SkyPulseError, APIError, LocationError
from .models import (
    WttrResponse,
    CurrentCondition,
    Weather,
    NearestArea,
    WeatherDesc,
    WeatherIconUrl,
    AreaName,
    Country,
    Region,
    WeatherUrl,
    Request,
    Astronomy,
    UnitPreferences
)

__all__ = [
    # Client classes
    "SkyPulse",
    "SkyPulseError",
    "APIError",
    "LocationError",
    
    # Model classes
    "WttrResponse",
    "CurrentCondition",
    "Weather",
    "NearestArea",
    "WeatherDesc",
    "WeatherIconUrl",
    "AreaName",
    "Country",
    "Region",
    "WeatherUrl",
    "Request",
    "Astronomy",
    "UnitPreferences",
    
    # Version info
    "__version__",
    "__prog__"
]
