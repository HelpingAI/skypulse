"""Command line interface for SkyPulse weather data."""

import sys
import argparse
from datetime import datetime
from typing import Optional, Dict, Any
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from rich.progress import Progress

from .client import SkyPulse, SkyPulseError
from .version import __version__, __prog__

console = Console()

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
    return Panel(table, title=f"Forecast for {day.date}", border_style="magenta")

def export_json(data: Dict[str, Any], filename: str):
    """Export weather data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    console.print(f"✓ Data exported to {filename}", style="green")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog=__prog__,
        description="🌤️  SkyPulse - Modern Weather Data CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("location", help="Location to get weather for")
    parser.add_argument("--version", action="version", version=f"SkyPulse {__version__}")
    
    # Weather data options
    data_group = parser.add_argument_group("Weather Data Options")
    data_group.add_argument("--forecast", "-f", action="store_true", help="Get weather forecast")
    data_group.add_argument("--days", "-d", type=int, default=3, choices=range(1, 11), help="Number of forecast days (1-10, default: 3)")
    data_group.add_argument("--detailed", "-D", action="store_true", help="Show detailed information")
    data_group.add_argument("--format", choices=["j1", "j2"], default="j2", help="API response format (default: j2)")
    data_group.add_argument("--alerts", "-a", action="store_true", help="Show weather alerts if available")
    
    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--json", "-j", action="store_true", help="Output raw JSON data")
    output_group.add_argument("--export", "-e", metavar="FILE", help="Export data to JSON file")
    output_group.add_argument("--no-color", action="store_true", help="Disable colored output")
    output_group.add_argument("--simple", "-s", action="store_true", help="Simple output format")
    
    args = parser.parse_args()
    
    if args.no_color:
        console.no_color = True

    try:
        with Progress(transient=True) as progress:
            task = progress.add_task("[cyan]Fetching weather data...", total=1)
            
            client = SkyPulse(format=args.format)
            
            if args.forecast:
                data = client.get_forecast(args.location, days=args.days)
                if args.json:
                    console.print_json(data.dict())
                else:
                    for day in data.days:
                        console.print(format_forecast_day(day, args.detailed))
            else:
                data = client.get_current(args.location)
                if args.json:
                    console.print_json(data.dict())
                elif args.simple:
                    console.print(f"[bold]{args.location}[/]: {data.temperature_c}°C, {data.condition.description}")
                else:
                    console.print(format_current_weather(data, args.location))
            
            if args.alerts and hasattr(data, 'alerts') and data.alerts:
                console.print("\n[bold red]⚠️ Weather Alerts[/]")
                for alert in data.alerts:
                    console.print(Panel(alert.description, title=alert.title, border_style="red"))
            
            if args.export:
                export_json(data.dict(), args.export)
            
            progress.update(task, completed=1)
            
    except SkyPulseError as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
