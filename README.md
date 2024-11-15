<div align="center">

# ☁️ SkyPulse

> A powerful, modern Python package for weather data retrieval with elegant API integration.

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/skypulse.svg)](https://badge.fury.io/py/skypulse)
[![License](https://img.shields.io/badge/License-HelpingAI%20v3.0-orange.svg)](LICENSE.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainer](https://img.shields.io/badge/maintainer-HelpingAI-blue)](https://github.com/HelpingAI)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [CLI Usage](#-cli-usage) • [Documentation](#-documentation) • [Examples](#-examples) • [Contributing](#-contributing)

---

</div>

## 🌟 Features

<div align="left">

- **🌍 Comprehensive Data**
  - Current weather conditions
  - Multi-day forecasts
  - Detailed astronomy data
  - Location information

- **🚀 Modern Architecture**
  - Async support with `aiohttp`
  - Type hints throughout
  - Pydantic models
  - Rich CLI interface

- **💪 Robust & Reliable**
  - Comprehensive error handling
  - Rate limiting support
  - Automatic retries
  - Detailed logging

- **🛠️ Developer Friendly**
  - Intuitive API design
  - Extensive documentation
  - Type completion support
  - Comprehensive examples

</div>

## 📦 Installation

<div align="left">

```bash
# Using pip (recommended)
pip install skypulse

# Using poetry
poetry add skypulse

# Development installation
git clone https://github.com/HelpingAI/skypulse.git
cd skypulse
pip install -e ".[dev]"
```

</div>

## 🚀 Quick Start

<div align="left">

```python
from skypulse import SkyPulse

# Initialize client
client = SkyPulse()

# Get current weather
current = client.get_current("London")
print(f"🌡️ Temperature: {current.temperature_c}°C ({current.temperature_f}°F)")
print(f"💧 Humidity: {current.humidity}%")
print(f"💨 Wind: {current.wind_speed_kmh} km/h {current.wind_direction}")

# Get detailed forecast
forecast = client.get_forecast("London", days=3)
for day in forecast.days:
    print(f"\n📅 {day.date}:")
    print(f"  🌡️ Temperature: {day.min_temp_c}°C to {day.max_temp_c}°C")
    print(f"  ☀️ UV Index: {day.uv_index}")
    print(f"  🌅 Sunrise: {day.astronomy.sunrise}")
    print(f"  🌇 Sunset: {day.astronomy.sunset}")
```

</div>

## 🖥️ CLI Usage

<div align="left">

SkyPulse comes with a powerful CLI for quick weather checks:

```bash
# Get current weather
skypulse "London"

# Get 5-day forecast with detailed info
skypulse "London" -f -d 5 -D

# Export to JSON
skypulse "London" -f --export weather.json
```

### CLI Options

<table>
<tr>
<th>Option</th>
<th>Description</th>
</tr>
<tr>
<td><code>--forecast, -f</code></td>
<td>Get weather forecast</td>
</tr>
<tr>
<td><code>--days, -d N</code></td>
<td>Number of forecast days (1-10)</td>
</tr>
<tr>
<td><code>--detailed, -D</code></td>
<td>Show detailed information</td>
</tr>
<tr>
<td><code>--format FMT</code></td>
<td>API format (j1 or j2)</td>
</tr>
<tr>
<td><code>--json, -j</code></td>
<td>Output raw JSON</td>
</tr>
<tr>
<td><code>--export, -e FILE</code></td>
<td>Export to JSON file</td>
</tr>
<tr>
<td><code>--no-color</code></td>
<td>Disable colored output</td>
</tr>
</table>

</div>

## 📚 Documentation

<div align="left">

### Data Models

<details>
<summary><b>Current Weather</b></summary>

```python
class Weather:
    temperature_c: float      # Temperature in Celsius
    temperature_f: float      # Temperature in Fahrenheit
    feels_like_c: float      # Feels like temperature
    humidity: int            # Humidity percentage
    wind_speed_kmh: float    # Wind speed in km/h
    wind_direction: str      # Wind direction (N, NE, etc.)
    pressure_mb: float       # Pressure in millibars
    uv_index: float         # UV index
    visibility_km: float    # Visibility in kilometers
    condition: WeatherCondition  # Weather condition details
```

</details>

<details>
<summary><b>Forecast</b></summary>

```python
class Forecast:
    days: List[ForecastDay]  # List of forecast days

class ForecastDay:
    date: str               # Date in YYYY-MM-DD format
    max_temp_c: float      # Maximum temperature
    min_temp_c: float      # Minimum temperature
    rain_chance: int       # Chance of rain (%)
    condition: WeatherCondition  # Weather condition
    astronomy: Astronomy   # Astronomical data
```

</details>

### API Reference

<details>
<summary><b>SkyPulse Client</b></summary>

```python
class SkyPulse:
    def get_current(location: str, format: str = "j1") -> Weather:
        """Get current weather for a location."""
        
    def get_forecast(location: str, format: str = "j1") -> Forecast:
        """Get weather forecast for a location."""
        
    def get_all(location: str, format: str = "j1") -> Dict[str, Any]:
        """Get all weather data for a location."""
```

</details>

</div>

## 🌈 Examples

<div align="left">

### Async Usage

```python
import asyncio
from skypulse import AsyncSkyPulse

async def get_weather():
    client = AsyncSkyPulse()
    weather = await client.get_current("London")
    print(f"Temperature: {weather.temperature_c}°C")

asyncio.run(get_weather())
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

### Custom API URL

```python
client = SkyPulse(api_url="https://your-custom-api.com/weather")
```

</div>

## 🤝 Contributing

<div align="left">

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔄 Open a Pull Request

</div>

## 📄 License

<div align="left">

This project is licensed under the HelpingAI License v3.0 - see the [LICENSE](LICENSE.md) file for details.

---

<div align="center">

Made with ❤️ by [HelpingAI](https://github.com/HelpingAI)

<a href="https://github.com/HelpingAI/skypulse/stargazers">⭐ Star us on GitHub</a> •
<a href="https://github.com/HelpingAI/skypulse/issues">📬 Report Bug</a> •
<a href="https://github.com/HelpingAI/skypulse/issues">✨ Request Feature</a>

</div>
