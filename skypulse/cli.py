"""Command line interface for SkyPulse - Modern Weather Data Package."""

import sys
import json
import locale
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.live import Live

from .client import SkyPulse, SkyPulseError
from .version import __version__, __prog__
from .ai_weather import WeatherAnalyzer

# Configure console for proper Unicode handling
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    
app = typer.Typer(
    name=__prog__,
    help="Modern Python weather data retrieval CLI",
    add_completion=True
)
console = Console(force_terminal=True)

def version_callback(value: bool):
    """Show version and exit."""
    if value:
        console.print(f"{__prog__} version: [cyan]{__version__}[/]")
        raise typer.Exit()

def create_weather_table(data: Dict[str, Any], location: str) -> Table:
    """Create a formatted table for weather data."""
    table = Table(title=f"Weather in {location}", show_header=True, border_style="cyan")
    table.add_column("Metric", style="cyan", justify="right")
    table.add_column("Value", style="green", justify="left")
    
    for key, value in data.items():
        if value not in ["N/A", None]:
            table.add_row(key, str(value))
    
    return table

def format_current_weather(current, location: str) -> Panel:
    """Format current weather data into a rich panel."""
    weather_data = {
        "Temperature": f"{current.temperature_c}°C ({current.temperature_f}°F)",
        "Feels Like": f"{current.feels_like_c}°C ({current.feels_like_f}°F)",
        "Condition": current.condition.description if hasattr(current, 'condition') else "N/A",
        "Humidity": f"{current.humidity}%",
        "Wind": f"{current.wind_speed_kmh} km/h {current.wind_direction}",
        "Pressure": f"{current.pressure_mb} mb",
        "UV Index": current.uv_index if hasattr(current, 'uv_index') else "N/A",
        "Visibility": f"{current.visibility_km} km" if hasattr(current, 'visibility_km') else "N/A",
        "Last Updated": current.last_updated if hasattr(current, 'last_updated') else "N/A"
    }
    
    table = create_weather_table(weather_data, location)
    return Panel(table, title="[bold cyan]Current Weather[/]", border_style="blue")

def format_forecast_day(day, detailed: bool = False) -> Panel:
    """Format forecast day data into a rich panel."""
    forecast_data = {
        "Temperature": f"{day.min_temp_c}°C to {day.max_temp_c}°C",
        "Condition": day.condition.description if hasattr(day, 'condition') else "N/A",
        "Rain Chance": f"{day.rain_chance}%" if hasattr(day, 'rain_chance') else "N/A",
        "UV Index": day.uv_index if hasattr(day, 'uv_index') else "N/A",
    }
    
    if detailed and hasattr(day, 'astronomy'):
        forecast_data.update({
            "Sunrise": day.astronomy.sunrise,
            "Sunset": day.astronomy.sunset,
            "Moon Phase": day.astronomy.moon_phase
        })
    
    table = create_weather_table(forecast_data, day.date)
    return Panel(table, title=f"[bold magenta]Forecast for {day.date}[/]", border_style="magenta")

def export_data(data: Dict[str, Any], format: str, filename: Optional[str] = None):
    """Export weather data to file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_data_{timestamp}.{format}"
    
    filepath = Path(filename)
    if format == "json":
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        raise ValueError(f"Unsupported export format: {format}")
    
    console.print(f"✓ Data exported to {filepath}", style="green")

@app.command()
def current(
    location: str = typer.Option(None, "--location", "-l", help="Location for weather data"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="API key for weather service", envvar="SKYPULSE_API_KEY"),
    export: str = typer.Option(None, "--export", "-e", help="Export data (json)"),
    version: bool = typer.Option(None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit"),
):
    """Get current weather conditions."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Fetching current weather...", total=None)
            client = SkyPulse(api_key)
            current = client.get_current(location)
            loc = f"{current.location.name}, {current.location.country}"
        
        console.print(format_current_weather(current, loc))
        
        if export:
            data = {
                "location": loc,
                "current": current.to_dict()
            }
            export_data(data, export)
            
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(1)

@app.command()
def forecast(
    location: str = typer.Option(None, "--location", "-l", help="Location for weather data"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="API key for weather service", envvar="SKYPULSE_API_KEY"),
    days: int = typer.Option(3, "--days", "-d", help="Number of forecast days"),
    detailed: bool = typer.Option(False, "--detailed", help="Show detailed information"),
    export: str = typer.Option(None, "--export", "-e", help="Export data (json)"),
):
    """Get weather forecast."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Fetching forecast...", total=None)
            client = SkyPulse(api_key)
            forecast = client.get_forecast(location, days=days)
            loc = f"{forecast.location.name}, {forecast.location.country}"
        
        panels: List[Panel] = []
        for day in forecast.days[:days]:
            panels.append(format_forecast_day(day, detailed))
        
        console.print(Columns(panels))
        
        if export:
            data = {
                "location": loc,
                "forecast": forecast.to_dict()
            }
            export_data(data, export)
            
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(1)

@app.command()
def analyze(
    location: str = typer.Option(None, "--location", "-l", help="Location for weather data"),
    api_key: str = typer.Option(None, "--api-key", "-k", help="API key for weather service", envvar="SKYPULSE_API_KEY"),
    openai_api_key: str = typer.Option(None, "--openai-key", help="OpenAI API key", envvar="OPENAI_API_KEY"),
):
    """Get AI-powered weather analysis and insights."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Analyzing weather data...", total=None)
            analyzer = WeatherAnalyzer(openai_api_key)
            weather_data = analyzer._get_weather_data(location)
            
        # Print AI analysis in real-time using sys.stdout
        console.print("\n", end="")  # Start with a newline
        for text in analyzer._get_ai_analysis(weather_data):
            sys.stdout.write(text)
            sys.stdout.flush()
        console.print("\n")  # End with a newline
            
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(1)

def main():
    """Main entry point for the CLI."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]An unexpected error occurred:[/] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
