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
      <li>Pydantic data models</li>
      <li>Context managers</li>
      <li>Rich CLI interface</li>
    </ul>
  </div>

  <div class="feature">
    <h3>🌡️ Comprehensive Weather Data</h3>
    <ul>
      <li>Real-time conditions</li>
      <li>Multi-day forecasts</li>
      <li>Astronomical data</li>
      <li>Location information</li>
      <li>Weather alerts</li>
    </ul>
  </div>

  <div class="feature">
    <h3>⚡ Flexible Usage</h3>
    <ul>
      <li>Sync/Async operations</li>
      <li>Custom API endpoints</li>
      <li>Format selection (j1/j2)</li>
      <li>Robust error handling</li>
      <li>Progress tracking</li>
    </ul>
  </div>

  <div class="feature">
    <h3>🛠️ Developer Experience</h3>
    <ul>
      <li>Comprehensive docs</li>
      <li>Type safety</li>
      <li>IDE completion</li>
      <li>Example code</li>
      <li>Testing support</li>
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
pip install -e ".[dev]"
```

### 📋 Requirements

- Python 3.7+
- Required packages:
  - `requests>=2.28.0`
  - `aiohttp>=3.8.0`
  - `pydantic>=2.0.0`
  - `rich>=12.0.0`
  - `typer>=0.7.0`

## 📖 Quick Start

### 🔄 Synchronous Usage
```python
from skypulse import SkyPulse

# Initialize client
client = SkyPulse()

# Get current weather
current = client.get_current("London")
print(f"Temperature: {current.temperature_c}°C")
print(f"Condition: {current.condition.description}")

# Get forecast
forecast = client.get_forecast("London", days=3)
for day in forecast.days:
    print(f"Date: {day.date}, Max: {day.max_temp_c}°C")
```

### ⚡ Asynchronous Usage
```python
import asyncio
from skypulse import SkyPulse

async def get_weather():
    async with SkyPulse(async_mode=True) as client:
        # Get current weather
        current = await client.get_current_async("London")
        print(f"Temperature: {current.temperature_c}°C")
        
        # Get forecast
        forecast = await client.get_forecast_async("London", days=3)
        for day in forecast.days:
            print(f"Date: {day.date}, Max: {day.max_temp_c}°C")

# Run async code
asyncio.run(get_weather())
```

### 🖥️ CLI Usage
```bash
# Get current weather
skypulse "London"

# Get 5-day forecast
skypulse "London" --forecast --days 5

# Get detailed weather with alerts
skypulse "London" --detailed --alerts

# Export weather data to JSON
skypulse "London" --export weather.json

# Simple output format
skypulse "London" --simple
```

## 📚 Documentation

### 🎯 Core Features

- **Location Support**: Search by city name
- **Data Formats**: Support for both j1 and j2 API response formats
- **Error Handling**: Comprehensive error handling with detailed messages
- **Rate Limiting**: Automatic rate limit handling with retries
- **Caching**: Optional response caching for improved performance

### 🔧 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `format` | str | "j2" | API response format (j1/j2) |
| `async_mode` | bool | False | Enable async operations |
| `cache_ttl` | int | 300 | Cache TTL in seconds |
| `timeout` | int | 10 | Request timeout in seconds |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🐛 **Report Bugs**: Open an [issue](https://github.com/HelpingAI/skypulse/issues)
2. 💡 **Suggest Features**: Share your ideas in [issues](https://github.com/HelpingAI/skypulse/issues)
3. 📝 **Documentation**: Help improve our docs
4. 🔧 **Code**: Submit [pull requests](https://github.com/HelpingAI/skypulse/pulls)

Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## 📊 Project Stats

<div align="center">
  <a href="https://github.com/HelpingAI/skypulse/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/HelpingAI/skypulse.svg" alt="Contributors">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/network/members">
    <img src="https://img.shields.io/github/forks/HelpingAI/skypulse.svg" alt="Forks">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/issues">
    <img src="https://img.shields.io/github/issues/HelpingAI/skypulse.svg" alt="Issues">
  </a>
  <a href="https://github.com/HelpingAI/skypulse/pulls">
    <img src="https://img.shields.io/github/issues-pr/HelpingAI/skypulse.svg" alt="Pull Requests">
  </a>
</div>

## 🔒 Security

Found a security issue? Please report it privately via:
- [GitHub Security Advisories](https://github.com/HelpingAI/skypulse/security/advisories)
- Email: helpingai5@gmail.com


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
