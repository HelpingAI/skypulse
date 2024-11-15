<div align="center">

# ☀️ SkyPulse

### Modern Python Weather Data Package with Async Support

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-HelpingAI-blue.svg)](LICENSE.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type Hints: mypy](https://img.shields.io/badge/type%20hints-mypy-blue.svg)](https://mypy.readthedocs.io/)

*A powerful Python library for weather data retrieval with both synchronous and asynchronous support.*

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Examples](#examples) • [Contributing](#contributing)

</div>

## ✨ Features

- **Modern Python Design**
  - Type hints throughout
  - Async and sync support
  - Pydantic models
  - Context managers
  - Rich CLI interface

- **Comprehensive Weather Data**
  - Current conditions
  - Multi-day forecasts
  - Astronomical data
  - Location information
  - Extended format support (j1/j2)

- **Flexible Usage**
  - Synchronous operations
  - Asynchronous operations
  - Custom API endpoints
  - Format selection
  - Error handling

- **Developer Experience**
  - Rich documentation
  - Type safety
  - IDE completion
  - Comprehensive examples
  - Testing support

## 🚀 Installation

### From PyPI
```bash
pip install skypulse
```

### Development Installation
```bash
git clone https://github.com/HelpingAI/skypulse.git
cd skypulse
pip install -e ".[dev]"
```

## 📖 Quick Start

### Synchronous Usage
```python
from skypulse import SkyPulse

# Initialize client
client = SkyPulse()

# Get current weather
current = client.get_current("London")
print(f"Temperature: {current.temperature_c}°C")
print(f"Condition: {current.condition.description}")

# Get forecast
forecast = client.get_forecast("London")
for day in forecast.days:
    print(f"Date: {day.date}, Max: {day.max_temp_c}°C")
```

### Asynchronous Usage
```python
import asyncio
from skypulse import SkyPulse

async def get_weather():
    async with SkyPulse(async_mode=True) as client:
        # Get current weather
        current = await client.get_current_async("London")
        print(f"Temperature: {current.temperature_c}°C")
        
        # Get forecast
        forecast = await client.get_forecast_async("London")
        for day in forecast.days:
            print(f"Date: {day.date}, Max: {day.max_temp_c}°C")

# Run async code
asyncio.run(get_weather())
```

## 📚 Documentation

### API Reference

<details>
<summary><b>SkyPulse Client</b></summary>

```python
class SkyPulse:
    def __init__(self, api_url: Optional[str] = None, async_mode: bool = False):
        """Initialize SkyPulse client."""
        
    def get_current(self, location: str, format: str = "j1") -> Weather:
        """Get current weather for a location."""
        
    async def get_current_async(self, location: str, format: str = "j1") -> Weather:
        """Get current weather for a location asynchronously."""
        
    def get_forecast(self, location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location."""
        
    async def get_forecast_async(self, location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location asynchronously."""
        
    def get_all(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Get all weather data for a location."""
        
    async def get_all_async(self, location: str, format: str = "j1") -> Dict[str, Any]:
        """Get all weather data for a location asynchronously."""
```
</details>

<details>
<summary><b>Weather Models</b></summary>

```python
@dataclass
class Weather:
    temperature_c: float
    temperature_f: float
    feels_like_c: float
    humidity: int
    wind_speed_kmh: float
    wind_direction: str
    condition: WeatherCondition

@dataclass
class Forecast:
    days: List[ForecastDay]

@dataclass
class Location:
    name: str
    country: str
    latitude: float
    longitude: float
```
</details>

### Data Formats

- **j1 (Basic)**
  - Current conditions
  - Basic forecast
  - Essential location data

- **j2 (Extended)**
  - Detailed conditions
  - Extended forecast
  - Astronomical data
  - Request metadata

## 🌈 Examples

### Custom API URL
```python
# Synchronous
client = SkyPulse(api_url="https://your-api-url.com")
weather = client.get_current("London")

# Asynchronous
async with SkyPulse(api_url="https://your-api-url.com", async_mode=True) as client:
    weather = await client.get_current_async("London")
```

### Error Handling
```python
from skypulse import SkyPulse, SkyPulseError, LocationError

try:
    client = SkyPulse()
    weather = client.get_current("NonexistentCity")
except LocationError as e:
    print(f"📍 Location error: {e}")
except SkyPulseError as e:
    print(f"⚠️ Weather error: {e}")
```

### Extended Format (j2)
```python
data = client.get_all("London", format="j2")
location = data["location"]
current = data["current"]
forecast = data["forecast"]

print(f"Location: {location.name}, {location.country}")
print(f"Temperature: {current.temperature_c}°C")
print(f"Condition: {current.condition.description}")

for day in forecast.days:
    print(f"\nDate: {day.date}")
    print(f"Temperature: {day.min_temp_c}°C to {day.max_temp_c}°C")
    print(f"Sunrise: {day.astronomy.sunrise}")
    print(f"Sunset: {day.astronomy.sunset}")
```

## 🛠️ Development

### Setup
```bash
# Clone repository
git clone https://github.com/HelpingAI/skypulse.git
cd skypulse

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

### Code Quality
```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
ruff check .
pylint skypulse
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the HelpingAI License v3.0 - see the [LICENSE](LICENSE.md) file for details.

---

<div align="center">

Made with ❤️ by [HelpingAI](https://github.com/HelpingAI)

</div>
