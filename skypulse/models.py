"""Weather data models for SkyPulse."""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UnitPreferences:
    """User preferences for units of measurement."""
    temperature: str = "C"  # C or F
    wind_speed: str = "kmh"  # kmh, mph, ms
    pressure: str = "mb"  # mb, in
    precipitation: str = "mm"  # mm, in
    distance: str = "km"  # km, mi

@dataclass
class WeatherDesc:
    """Weather description."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WeatherDesc":
        return cls(value=data["value"])

@dataclass
class WeatherIconUrl:
    """Weather icon URL."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WeatherIconUrl":
        return cls(value=data["value"])

@dataclass
class AreaName:
    """Area name."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AreaName":
        return cls(value=data["value"])

@dataclass
class Country:
    """Country name."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Country":
        return cls(value=data["value"])

@dataclass
class Region:
    """Region name."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Region":
        return cls(value=data["value"])

@dataclass
class WeatherUrl:
    """Weather URL."""
    value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WeatherUrl":
        return cls(value=data["value"])

@dataclass
class Request:
    """API request details."""
    type: str
    query: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Request":
        return cls(
            type=data["type"],
            query=data["query"]
        )

@dataclass
class Astronomy:
    """Astronomy data."""
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Astronomy":
        return cls(
            sunrise=data["sunrise"],
            sunset=data["sunset"],
            moonrise=data["moonrise"],
            moonset=data["moonset"],
            moon_phase=data["moon_phase"],
            moon_illumination=data["moon_illumination"]
        )

@dataclass
class CurrentCondition:
    """Current weather conditions."""
    observation_time: str
    temp_C: str
    temp_F: str
    weatherCode: str
    weatherIconUrl: List[WeatherIconUrl]
    weatherDesc: List[WeatherDesc]
    windspeedMiles: str
    windspeedKmph: str
    winddirDegree: str
    winddir16Point: str
    precipMM: str
    precipInches: str
    humidity: str
    visibility: str
    visibilityMiles: str
    pressure: str
    pressureInches: str
    cloudcover: str
    FeelsLikeC: str
    FeelsLikeF: str
    uvIndex: str
    localObsDateTime: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CurrentCondition":
        return cls(
            observation_time=data["observation_time"],
            temp_C=data["temp_C"],
            temp_F=data["temp_F"],
            weatherCode=data["weatherCode"],
            weatherIconUrl=[WeatherIconUrl.from_dict(x) for x in data["weatherIconUrl"]],
            weatherDesc=[WeatherDesc.from_dict(x) for x in data["weatherDesc"]],
            windspeedMiles=data["windspeedMiles"],
            windspeedKmph=data["windspeedKmph"],
            winddirDegree=data["winddirDegree"],
            winddir16Point=data["winddir16Point"],
            precipMM=data["precipMM"],
            precipInches=data["precipInches"],
            humidity=data["humidity"],
            visibility=data["visibility"],
            visibilityMiles=data["visibilityMiles"],
            pressure=data["pressure"],
            pressureInches=data["pressureInches"],
            cloudcover=data["cloudcover"],
            FeelsLikeC=data["FeelsLikeC"],
            FeelsLikeF=data["FeelsLikeF"],
            uvIndex=data["uvIndex"],
            localObsDateTime=data.get("localObsDateTime", data.get("observation_time", ""))
        )

@dataclass
class NearestArea:
    """Nearest area information."""
    latitude: str
    longitude: str
    population: str
    areaName: List[AreaName]
    country: List[Country]
    region: List[Region]
    weatherUrl: List[WeatherUrl]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NearestArea":
        return cls(
            latitude=data["latitude"],
            longitude=data["longitude"],
            population=data["population"],
            areaName=[AreaName.from_dict(x) for x in data["areaName"]],
            country=[Country.from_dict(x) for x in data["country"]],
            region=[Region.from_dict(x) for x in data["region"]],
            weatherUrl=[WeatherUrl.from_dict(x) for x in data["weatherUrl"]]
        )

@dataclass
class Weather:
    """Weather forecast data."""
    date: str
    astronomy: List[Astronomy]
    maxtempC: str
    maxtempF: str
    mintempC: str
    mintempF: str
    avgtempC: str
    avgtempF: str
    totalSnow_cm: str
    sunHour: str
    uvIndex: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Weather":
        return cls(
            date=data["date"],
            astronomy=[Astronomy.from_dict(x) for x in data["astronomy"]],
            maxtempC=data["maxtempC"],
            maxtempF=data["maxtempF"],
            mintempC=data["mintempC"],
            mintempF=data["mintempF"],
            avgtempC=data["avgtempC"],
            avgtempF=data["avgtempF"],
            totalSnow_cm=data["totalSnow_cm"],
            sunHour=data["sunHour"],
            uvIndex=data["uvIndex"]
        )

@dataclass
class WttrResponse:
    """Full weather response."""
    request: List[Request]
    current_condition: List[CurrentCondition]
    nearest_area: List[NearestArea]
    weather: List[Weather]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WttrResponse":
        return cls(
            request=[Request.from_dict(x) for x in data.get("request", [])],
            current_condition=[CurrentCondition.from_dict(x) for x in data.get("current_condition", [])],
            nearest_area=[NearestArea.from_dict(x) for x in data.get("nearest_area", [])],
            weather=[Weather.from_dict(x) for x in data.get("weather", [])]
        )
