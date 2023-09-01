from typing import Any, Callable
from functools import partial
import requests
from pydantic import BaseModel

CONFIG_PATH = "config_video.json"
HttpGet = Callable[[str], Any]


class CityNotFoundError(Exception):
    pass


class UrlTemplateClient(BaseModel):
    template: str

    def get(self, data: dict[str, Any]) -> dict[str, Any]:
        url = self.template.format(**data)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()


def create_client() -> UrlTemplateClient:
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = UrlTemplateClient.model_validate_json(file.read())
    return config


def get_forecast(city: str, client: UrlTemplateClient) -> dict[str, Any]:
    response = client.get({"city": city})
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def get_humidity(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["main"]["humidity"]


def get_wind_speed(full_weather_forecast: dict[str, Any]) -> float:
    return full_weather_forecast["wind"]["speed"]


def get_wind_direction(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["wind"]["deg"]


def main() -> None:
    get_weather = partial(get_forecast, client=create_client())

    city = "Utrecht"

    weather_forecast = get_weather(city)

    print(
        f"The current temperature in {city} is {get_temperature(weather_forecast):.1f} °C."
    )
    print(f"The current humidity in {city} is {get_humidity(weather_forecast)}%.")
    print(
        f"The current wind speed in {city} is {get_wind_speed(weather_forecast) } m/s from direction {get_wind_direction(weather_forecast)} degrees."
    )


if __name__ == "__main__":
    main()
