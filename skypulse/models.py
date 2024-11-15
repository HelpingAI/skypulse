"""WeatherFlow data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any, Union

@dataclass
class RequestInfo:
    """Request information (v2 format only)."""
    query: str
    type: str

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'RequestInfo':
        """Create RequestInfo from API response data."""
        return cls(
            query=data.get('query', ''),
            type=data.get('type', '')
        )

@dataclass
class Location:
    """Location data."""
    name: str
    country: str
    region: str
    latitude: float
    longitude: float
    population: int
    weather_url: str

    @classmethod
    def from_data(cls, data: Union[List[Dict[str, Any]], Dict[str, Any]], format: str = "j1") -> 'Location':
        """Create Location from API response data."""
        if not data:
            return cls("Unknown", "Unknown", "Unknown", 0.0, 0.0, 0, "")

        # Handle both list (v1) and direct object (v2) formats
        loc = data[0] if isinstance(data, list) else data
        return cls(
            name=loc.get('name', 'Unknown'),
            country=loc.get('country', 'Unknown'),
            region=loc.get('region', 'Unknown'),
            latitude=float(loc.get('latitude', 0)),
            longitude=float(loc.get('longitude', 0)),
            population=int(loc.get('population', 0)),
            weather_url=loc.get('weather_url', '')
        )

@dataclass
class WeatherCondition:
    """Weather condition data."""
    code: int
    description: str
    icon_url: str

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'WeatherCondition':
        """Create WeatherCondition from API response data."""
        return cls(
            code=int(data.get('code', 0)),
            description=data.get('description', 'Unknown'),
            icon_url=data.get('icon_url', '')
        )

@dataclass
class Astronomy:
    """Astronomical data."""
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: int

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'Astronomy':
        """Create Astronomy from API response data."""
        return cls(
            sunrise=data.get('sunrise', '06:00 AM'),
            sunset=data.get('sunset', '06:00 PM'),
            moonrise=data.get('moonrise', '12:00 PM'),
            moonset=data.get('moonset', '12:00 AM'),
            moon_phase=data.get('moon_phase', 'Unknown'),
            moon_illumination=int(data.get('moon_illumination', 0))
        )

@dataclass
class HourlyForecast:
    """Hourly forecast data."""
    time: str
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    feels_like_f: float
    wind_speed_kmh: float
    wind_speed_mph: float
    wind_direction: str
    wind_degree: int
    wind_gust_kmh: float
    wind_gust_mph: float
    pressure_mb: int
    pressure_in: float
    humidity: int
    cloud_cover: int
    rain_chance: int
    snow_chance: int
    visibility: int
    visibility_miles: int
    uv_index: int
    dew_point_c: float
    dew_point_f: float
    heat_index_c: float
    heat_index_f: float
    wind_chill_c: float
    wind_chill_f: float
    condition: WeatherCondition

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'HourlyForecast':
        """Create HourlyForecast from API response data."""
        return cls(
            time=data.get('time', '0'),
            temperature_c=float(data.get('temperature_c', 0)),
            temperature_f=float(data.get('temperature_f', 0)),
            feels_like_c=float(data.get('feels_like_c', 0)),
            feels_like_f=float(data.get('feels_like_f', 0)),
            wind_speed_kmh=float(data.get('wind_speed_kmh', 0)),
            wind_speed_mph=float(data.get('wind_speed_mph', 0)),
            wind_direction=data.get('wind_direction', 'N'),
            wind_degree=int(data.get('wind_degree', 0)),
            wind_gust_kmh=float(data.get('wind_gust_kmh', 0)),
            wind_gust_mph=float(data.get('wind_gust_mph', 0)),
            pressure_mb=int(data.get('pressure_mb', 0)),
            pressure_in=float(data.get('pressure_in', 0)),
            humidity=int(data.get('humidity', 0)),
            cloud_cover=int(data.get('cloud_cover', 0)),
            rain_chance=int(data.get('rain_chance', 0)),
            snow_chance=int(data.get('snow_chance', 0)),
            visibility=int(data.get('visibility', 0)),
            visibility_miles=int(data.get('visibility_miles', 0)),
            uv_index=int(data.get('uv_index', 0)),
            dew_point_c=float(data.get('dew_point_c', 0)),
            dew_point_f=float(data.get('dew_point_f', 0)),
            heat_index_c=float(data.get('heat_index_c', 0)),
            heat_index_f=float(data.get('heat_index_f', 0)),
            wind_chill_c=float(data.get('wind_chill_c', 0)),
            wind_chill_f=float(data.get('wind_chill_f', 0)),
            condition=WeatherCondition.from_data(data.get('condition', {}))
        )

@dataclass
class ForecastDay:
    """Daily forecast data."""
    date: str
    max_temp_c: float
    max_temp_f: float
    min_temp_c: float
    min_temp_f: float
    avg_temp_c: float
    avg_temp_f: float
    total_snow_cm: float
    sun_hour: float
    uv_index: int
    hourly: List[HourlyForecast]
    astronomy: Astronomy

    @classmethod
    def from_data(cls, data: Dict[str, Any]) -> 'ForecastDay':
        """Create ForecastDay from API response data."""
        return cls(
            date=data.get('date', ''),
            max_temp_c=float(data.get('max_temp_c', 0)),
            max_temp_f=float(data.get('max_temp_f', 0)),
            min_temp_c=float(data.get('min_temp_c', 0)),
            min_temp_f=float(data.get('min_temp_f', 0)),
            avg_temp_c=float(data.get('avg_temp_c', 0)),
            avg_temp_f=float(data.get('avg_temp_f', 0)),
            total_snow_cm=float(data.get('total_snow_cm', 0)),
            sun_hour=float(data.get('sun_hour', 0)),
            uv_index=int(data.get('uv_index', 0)),
            hourly=[HourlyForecast.from_data(h) for h in data.get('hourly', [])],
            astronomy=Astronomy.from_data(data.get('astronomy', {}))
        )

@dataclass
class Forecast:
    """Weather forecast data."""
    days: List[ForecastDay]

    @classmethod
    def from_data(cls, data: Dict[str, Any], format: str = "j1") -> 'Forecast':
        """Create Forecast from API response data."""
        return cls(
            days=[ForecastDay.from_data(day) for day in data.get('days', [])]
        )

@dataclass
class Weather:
    """Current weather data."""
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    feels_like_f: float
    wind_speed_kmh: float
    wind_speed_mph: float
    wind_direction: str
    wind_degree: int
    pressure_mb: int
    pressure_in: float
    humidity: int
    cloud_cover: int
    visibility: int
    visibility_miles: int
    uv_index: int
    local_obs_time: Optional[str]
    condition: WeatherCondition

    @classmethod
    def from_data(cls, data: Dict[str, Any], format: str = "j1") -> 'Weather':
        """Create Weather from API response data."""
        return cls(
            temperature_c=float(data.get('temperature_c', 0)),
            temperature_f=float(data.get('temperature_f', 0)),
            feels_like_c=float(data.get('feels_like_c', 0)),
            feels_like_f=float(data.get('feels_like_f', 0)),
            wind_speed_kmh=float(data.get('wind_speed_kmh', 0)),
            wind_speed_mph=float(data.get('wind_speed_mph', 0)),
            wind_direction=data.get('wind_direction', 'N'),
            wind_degree=int(data.get('wind_degree', 0)),
            pressure_mb=int(data.get('pressure_mb', 0)),
            pressure_in=float(data.get('pressure_in', 0)),
            humidity=int(data.get('humidity', 0)),
            cloud_cover=int(data.get('cloud_cover', 0)),
            visibility=int(data.get('visibility', 0)),
            visibility_miles=int(data.get('visibility_miles', 0)),
            uv_index=int(data.get('uv_index', 0)),
            local_obs_time=data.get('local_obs_time'),
            condition=WeatherCondition.from_data(data.get('condition', {}))
        )
