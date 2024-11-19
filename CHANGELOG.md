# Changelog

All notable changes to the SkyPulse project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-01-17

### Added
- Complete integration with wttr.in API for reliable weather data
- Comprehensive data models using Python dataclasses
- Support for both j1 (detailed) and j2 (condensed) formats
- AI-powered weather analysis with OpenAI integration
- Natural language processing for weather insights
- Activity suggestions based on weather conditions
- Weather pattern detection and trend analysis
- Location comparison functionality
- Cross-platform Unicode support
- Progress indicators for long-running operations
- Type-safe data handling throughout
- Custom unit preferences system
- Concurrent location comparison

### Changed
- Switched to wttr.in as primary weather data provider
- Improved error handling with custom exceptions
- Enhanced documentation with new features and examples
- Updated CLI interface with better formatting
- Restructured project for better maintainability
- Optimized async operations
- Improved type hints coverage

### Fixed
- Unicode rendering issues on Windows
- Real-time data streaming in async mode
- Environment variable handling
- Location validation and error reporting
- Type conversion edge cases
- Memory usage in concurrent operations

### Development
- Added comprehensive test suite
- Implemented CI/CD pipeline
- Added code quality tools (black, isort, mypy)
- Improved development documentation
- Added pre-commit hooks
- Enhanced build system

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

[1.1.0]: https://github.com/HelpingAI/skypulse/releases/tag/v1.1.0
[1.0.0]: https://github.com/HelpingAI/skypulse/releases/tag/v1.0.0
