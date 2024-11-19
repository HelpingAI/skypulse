"""
SkyPulse - Modern Weather Data Package
A powerful Python library for weather data retrieval with AI capabilities
Copyright (c) 2024 HelpingAI. All rights reserved.
Licensed under the HelpingAI License v3.0
"""

from setuptools import setup, find_packages
import os

# Read version from version.py
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "skypulse", "version.py"), encoding="utf-8") as f:
    exec(f.read(), about)

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=about["__prog__"],
    version=about["__version__"],
    author="HelpingAI",
    author_email="helpingai5@gmail.com",
    description="Modern Python weather data retrieval library with async support and AI analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HelpingAI/skypulse",
    project_urls={
        "Bug Tracker": "https://github.com/HelpingAI/skypulse/issues",
        "Documentation": "https://github.com/HelpingAI/skypulse#readme",
        "Source": "https://github.com/HelpingAI/skypulse",
        "Changelog": "https://github.com/HelpingAI/skypulse/blob/main/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Framework :: AsyncIO",
        "Natural Language :: English",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.2",
        "aiohttp>=3.8.4",
        "pydantic>=2.0.0",
        "typing-extensions>=4.5.0",
        "python-dateutil>=2.8.2",
        "openai>=1.3.0",
        "rich>=13.3.5",
        "typer>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.20.0",
            "black>=22.0.0",
            "isort>=5.10.0",
            "mypy>=0.990",
            "ruff>=0.0.290",
            "pre-commit>=3.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skypulse=skypulse.cli:main",
        ],
    },
    keywords=[
        "weather",
        "wttr.in",
        "async",
        "api",
        "climate",
        "forecast",
        "meteorology",
        "python",
        "ai",
        "artificial-intelligence",
        "machine-learning",
        "nlp",
        "natural-language-processing",
        "weather-analysis",
        "weather-ai",
        "weather-forecast",
        "weather-data",
        "weather-api",
        "asyncio",
        "real-time",
        "openai",
        "helpingai",
    ],
    include_package_data=True,
    zip_safe=False,
)
