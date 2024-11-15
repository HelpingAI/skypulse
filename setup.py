"""
SkyPulse - Modern Weather Data Package
Copyright (c) 2024 HelpingAI. All rights reserved.
Licensed under the HelpingAI License v3.0
"""

from setuptools import setup, find_packages
import os
from weatherflow.version import __version__, __prog__
# Read README for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=__prog__,
    version=__version__,
    author="HelpingAI",
    author_email="helpingai5@gmail.com",
    description="A powerful Python package for weather data retrieval with elegant API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HelpingAI/skypulse",
    packages=find_packages(),
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
        "Framework :: AsyncIO",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "typing-extensions>=4.0.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "ruff>=0.1.0",
            "pre-commit>=3.4.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
            "myst-parser>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skypulse=weatherflow.cli:main",
        ],
    },
    keywords=[
        "weather",
        "api",
        "forecast",
        "meteorology",
        "climate",
        "weather-api",
        "weather-data",
        "weather-forecast",
        "async",
        "skypulse",
    ],
    project_urls={
        "Documentation": "https://github.com/HelpingAI/skypulse",
        "Source": "https://github.com/HelpingAI/skypulse",
        "Issues": "https://github.com/HelpingAI/skypulse/issues",
        "Changelog": "https://github.com/HelpingAI/skypulse/blob/main/CHANGELOG.md",
    },
    package_data={
        "weatherflow": ["py.typed"],
    },
    zip_safe=False,
    license="HelpingAI License v3.0",
)
