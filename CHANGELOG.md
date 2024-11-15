# Changelog

All notable changes to the SkyPulse project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-15

### Added
- Initial release of SkyPulse weather data package
- Modern Python weather data retrieval library
- Full async support with context managers
- Comprehensive CLI interface with rich formatting
- Support for both basic (j1) and extended (j2) API formats
- Current weather conditions retrieval (sync/async)
- Multi-day forecast support (sync/async)
- Astronomical data integration
- Location information handling
- Type hints throughout the codebase
- Pydantic models for data validation
- Comprehensive error handling system

### Features
- Both synchronous and asynchronous APIs
- Rich, color-coded CLI output
- JSON export capabilities
- Detailed and summary view options
- Flexible querying options
- Custom API URL support
- Configurable output formats
- Cross-platform compatibility
- Async context manager support
- Session management for both sync/async

### Dependencies
- Core: requests, aiohttp, pydantic, typing-extensions, python-dateutil
- CLI: rich, typer
- Async: aiohttp, asyncio

### Development
- Setup configuration with setup.py
- Development installation support
- Comprehensive test suite with async tests
- Modern Python packaging practices
- Type-safe implementations
- Async-aware error handling

[1.0.0]: https://github.com/HelpingAI/skypulse/releases/tag/v1.0.0
