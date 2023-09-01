import os
from typing import Any, Protocol

import requests
from dotenv import load_dotenv


class CityNotFoundError(Exception):
    pass


class HttpClient(Protocol):
    def get(self, url: str) -> dict[str, Any]:
        ...


class RequestsClient:
    def get(self, url: str) -> dict[str, Any]:
        response = requests.get(url, timeout=5)
        return response.json()


def get(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=5)
    return response.json()


class WeatherApi:
    def __init__(self, client: HttpClient, api_key: str) -> None:
        self.client = client
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.client.get(url)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response

    @property
    def temperature(self) -> float:
        temperature = self.full_weather_forecast["main"]["temp"]
        return temperature - 273.15  # convert from Kelvin to Celsius

    @property
    def humidity(self) -> int:
        return self.full_weather_forecast["main"]["humidity"]

    @property
    def wind_speed(self) -> float:
        return self.full_weather_forecast["wind"]["speed"]

    @property
    def wind_direction(self) -> int:
        return self.full_weather_forecast["wind"]["deg"]


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    city = "Utrecht"

    if api_key:
        weather = WeatherApi(RequestsClient(), api_key=api_key)
        weather.retrieve_forecast(city)
        print(f"The current temperature in {city} is {weather.temperature:.1f} °C.")
        print(f"The current humidity in {city} is {weather.humidity}%.")
        print(
            f"The current wind speed in {city} is {weather.wind_speed} m/s from direction {weather.wind_direction} degrees."
        )
    else:
        print("Please set the environment variable OPENWEATHERMAP_API_KEY")
        return


if __name__ == "__main__":
    main()
