import os
from typing import Any, Callable
from functools import partial

import requests
from dotenv import load_dotenv


class CityNotFoundError(Exception):
    pass


def get(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


HttpGet = Callable[[str], Any]


def get_forecast(request_func: HttpGet, api_key: str, city: str) -> dict[str, Any]:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = request_func(url)
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def get_temperature(forecast: dict[str, Any]) -> float:
    temperature = forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def get_humidity(forecast: dict[str, Any]) -> int:
    return forecast["main"]["humidity"]


def get_wind_speed(forecast: dict[str, Any]) -> float:
    return forecast["wind"]["speed"]


def get_wind_direction(forecast: dict[str, Any]) -> int:
    return forecast["wind"]["deg"]


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    city = "Utrecht"

    if api_key:
        get_forecast_partial = partial(get_forecast, get, api_key)
        forecast = get_forecast_partial(city)
        print(
            f"The current temperature in {city} is {get_temperature(forecast):.1f} °C."
        )
        print(f"The current humidity in {city} is {get_humidity(forecast)}%.")
        print(
            f"The current wind speed in {city} is {get_wind_speed(forecast)} m/s "
            f"from direction {get_wind_direction(forecast)} degrees."
        )
    else:
        print("Please set the environment variable OPENWEATHERMAP_API_KEY")
        return


if __name__ == "__main__":
    main()
