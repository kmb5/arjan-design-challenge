from typing import Any, Protocol
import os
import requests
from dotenv import load_dotenv


class CityNotFoundError(Exception):
    pass


class WeatherServiceCreationError(Exception):
    pass


class HTTPClient(Protocol):
    def get(self, url: str) -> Any:
        ...


class RequestsClient:
    def get(self, url: str) -> Any:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()


class WeatherService:
    def __init__(self, client: HTTPClient, api_key: str) -> None:
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
        return temperature - 273.15

    @property
    def humidity(self) -> float:
        return self.full_weather_forecast["main"]["humidity"]

    @property
    def wind_speed(self) -> float:
        return self.full_weather_forecast["wind"]["speed"]

    @property
    def wind_direction(self) -> float:
        return self.full_weather_forecast["wind"]["deg"]


class WeatherServiceFactory:
    @staticmethod
    def create_weather_service(client: HTTPClient) -> WeatherService:
        load_dotenv()
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if api_key:
            return WeatherService(client=client, api_key=api_key)
        else:
            raise WeatherServiceCreationError(
                "No API key found, please set OPENWEATHERMAP_API_KEY in .env file."
            )


def main() -> None:
    city = "Utrecht"

    http_client = RequestsClient()
    client = WeatherServiceFactory.create_weather_service(client=http_client)
    client.retrieve_forecast(city=city)
    print(f"The current temperature in {city} is {client.temperature:.1f} °C.")
    print(f"The current humidity in {city} is {client.humidity}%.")
    print(
        f"The current wind speed in {city} is {client.wind_speed} m/s from direction {client.wind_direction} degrees."
    )


if __name__ == "__main__":
    main()
