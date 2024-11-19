<div align="center">

# ☀️ SkyPulse

<h3>Modern Python Weather Data Package with Async Support</h3>

<div align="center">
  <a href="https://pypi.org/project/skypulse/">
    <img src="https://img.shields.io/pypi/v/skypulse.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/skypulse/">
    <img src="https://img.shields.io/pypi/pyversions/skypulse.svg" alt="Python versions">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/actions">
    <img src="https://github.com/HelpingAI/skypulse/workflows/tests/badge.svg" alt="Tests">
  </a>
  <a href="https://codecov.io/gh/HelpingAI/skypulse">
    <img src="https://codecov.io/gh/HelpingAI/skypulse/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  </a>
  <a href="https://pycqa.github.io/isort/">
    <img src="https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336" alt="Imports: isort">
  </a>
  <a href="https://mypy.readthedocs.io/">
    <img src="https://img.shields.io/badge/type%20hints-mypy-blue.svg" alt="Type Hints: mypy">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/blob/main/LICENSE.md">
    <img src="https://img.shields.io/github/license/HelpingAI/skypulse.svg" alt="License">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/stargazers">
    <img src="https://img.shields.io/github/stars/HelpingAI/skypulse.svg" alt="GitHub stars">
  </a>
  <a href="https://pepy.tech/project/skypulse">
    <img src="https://pepy.tech/badge/skypulse" alt="Downloads">
  </a>
  <a href="https://discord.gg/helpingai">
    <img src="https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white" alt="Discord">
  </a>
</div>

<p align="center">
  <i>A powerful Python library for weather data retrieval with both synchronous and asynchronous support.</i>
</p>

<div align="center">
  <h3>
    <a href="#features">Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#documentation">Documentation</a> •
    <a href="#contributing">Contributing</a>
  </h3>
</div>

</div>

## ✨ Features

<div class="grid">
  <div class="feature">
    <h3>🔄 Modern Python Design</h3>
    <ul>
      <li>Full type hints support</li>
      <li>Async and sync operations</li>
      <li>Dataclass-style models</li>
      <li>Context managers</li>
      <li>Clean API interface</li>
    </ul>
  </div>

  <div class="feature">
    <h3>🌡️ Weather Data</h3>
    <ul>
      <li>Current weather conditions</li>
      <li>Detailed forecasts</li>
      <li>Hourly predictions</li>
      <li>Astronomical data</li>
      <li>Wind information</li>
    </ul>
  </div>

  <div class="feature">
    <h3>⚡ Flexible Usage</h3>
    <ul>
      <li>Sync/Async operations</li>
      <li>Custom API endpoints</li>
      <li>Format selection (j1/j2)</li>
      <li>Unit preferences</li>
      <li>Multi-location support</li>
    </ul>
  </div>

  <div class="feature">
    <h3>🛠️ Developer Experience</h3>
    <ul>
      <li>Type safety</li>
      <li>Error handling</li>
      <li>Data validation</li>
      <li>Easy integration</li>
      <li>Modular design</li>
    </ul>
  </div>
</div>

## 🚀 Installation

### 📦 From PyPI
```bash
pip install skypulse
```

### 🔧 Development Installation
```bash
git clone https://github.com/HelpingAI/skypulse.git
cd skypulse
pip install -e .
```

### 📋 Requirements

- Python 3.7+
- Required packages:
  - `requests>=2.28.2` - HTTP requests for sync operations
  - `aiohttp>=3.8.4` - Async HTTP client

## 📖 Quick Start

### 🔄 Synchronous Usage
```python
from skypulse import SkyPulse, UnitPreferences

# Initialize client
client = SkyPulse()

# Set unit preferences (optional)
client.set_units(UnitPreferences(
    temperature="C",
    wind_speed="kmh",
    pressure="mb"
))

# Get current weather
current = client.get_current("London")
print(f"Temperature: {current.temperature_c}°C")
print(f"Condition: {current.condition.description}")
print(f"Wind: {current.wind_speed_kmh} km/h {current.wind_direction}")
print(f"Humidity: {current.humidity}%")

# Get forecast with hourly data
forecast = client.get_forecast("London")
for day in forecast.days:
    print(f"\nDate: {day.date}")
    print(f"Temperature: {day.min_temp_c}°C to {day.max_temp_c}°C")
    print(f"Sunrise: {day.astronomy.sunrise}")
    print(f"Sunset: {day.astronomy.sunset}")
    
    # Hourly forecast
    for hour in day.hourly:
        print(f"\nTime: {hour.time}")
        print(f"Temperature: {hour.temperature_c}°C")
        print(f"Feels like: {hour.feels_like_c}°C")
        print(f"Rain chance: {hour.rain_chance}%")
```

### ⚡ Asynchronous Usage
```python
import asyncio
from skypulse import SkyPulse

async def compare_weather():
    async with SkyPulse(async_mode=True) as client:
        # Compare weather for multiple cities concurrently
        cities = ["London", "New York", "Tokyo"]
        tasks = [client.get_current_async(city) for city in cities]
        results = await asyncio.gather(*tasks)
        
        for city, weather in zip(cities, results):
            print(f"\n{city}:")
            print(f"Temperature: {weather.temperature_c}°C")
            print(f"Condition: {weather.condition.description}")
            print(f"Humidity: {weather.humidity}%")

# Run async code
asyncio.run(compare_weather())
```

## 📚 Core Features

### Current Weather
- Real-time temperature and humidity
- Wind speed, direction, and gusts
- Atmospheric pressure
- Cloud cover and visibility
- Weather conditions with icons

### Weather Forecast
- Multi-day weather forecasts
- Hourly predictions
- Temperature ranges
- Rain and snow chances
- Astronomical data (sunrise/sunset)

### Location Support
- City name or coordinates
- Country and region info
- Latitude and longitude
- Population data
- Weather station URL

### Unit Preferences
- Temperature (°C/°F)
- Wind speed (km/h, mph)
- Pressure (mb, in)
- Distance (km, miles)
- Precipitation (mm, in)

### AI Analysis
- Real-time weather insights
- Natural language analysis
- Activity suggestions
- Weather pattern detection
- Streaming responses
- Cross-platform Unicode support

## 🤖 AI Usage
```python
from skypulse.ai_weather import WeatherAnalyzer

# Initialize analyzer
analyzer = WeatherAnalyzer()

# Get AI analysis
analysis = analyzer.analyze_weather("Tokyo")
print(analysis)

# CLI usage
skypulse analyze --location "Tokyo"
```

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the HelpingAI License v3.0 - see the [LICENSE](LICENSE.md) file for details.

<div align="center">

---

<p>
  Made with ❤️ by <a href="https://github.com/HelpingAI">HelpingAI</a>
</p>

<p>
  <a href="https://github.com/HelpingAI/skypulse/blob/main/LICENSE.md">HelpingAI License</a> •
  <a href="https://github.com/HelpingAI/skypulse/blob/main/CODE_OF_CONDUCT.md">Code of Conduct</a> •
  <a href="https://github.com/HelpingAI/skypulse/blob/main/SECURITY.md">Security Policy</a>
</p>

</div>
