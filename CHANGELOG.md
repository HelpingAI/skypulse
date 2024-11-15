# Changelog

All notable changes to the SkyPulse project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-15

### Added
- Initial release of SkyPulse weather data package
- Modern Python weather data retrieval library
- Comprehensive CLI interface with rich formatting
- Support for both basic (j1) and extended (j2) API formats
- Current weather conditions retrieval
- Multi-day forecast support
- Astronomical data integration
- Location information handling
- Async support preparation
- Type hints throughout the codebase
- Pydantic models for data validation
- Comprehensive error handling system

### Features
- Rich, color-coded CLI output
- JSON export capabilities
- Detailed and summary view options
- Flexible querying options
- Custom API URL support
- Configurable output formats
- Cross-platform compatibility

### Dependencies
- Core: requests, typing-extensions, aiohttp, pydantic, python-dateutil
- CLI: rich, typer

### Development
- Setup configuration with setup.py
- Development installation support
- Comprehensive test suite
- Modern Python packaging practices
- Type-safe implementations

[1.0.0]: https://github.com/HelpingAI/skypulse/releases/tag/v1.0.0
