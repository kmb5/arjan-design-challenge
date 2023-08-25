from typing import Any, Optional
import os
import requests
from dotenv import load_dotenv


class CityNotFoundError(Exception):
    pass


class WeatherServiceCreationError(Exception):
    pass


class RequestsClient:
    def get(self, url: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        return requests.get(url, params=params, timeout=5).json()


class WeatherService:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}

    def retrieve_forecast(self, city: str, request_client: RequestsClient) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = request_client.get(url)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response


class WeatherServiceFactory:
    @staticmethod
    def create_weather_service() -> WeatherService:
        load_dotenv()
        api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if api_key:
            return WeatherService(api_key=api_key)
        else:
            raise WeatherServiceCreationError(
                "No API key found, please set OPENWEATHERMAP_API_KEY in .env file."
            )


def main() -> None:
    city = "Utrecht"

    client = WeatherServiceFactory.create_weather_service()
    request_client = RequestsClient()
    client.retrieve_forecast(city=city, request_client=request_client)
    temp = client.full_weather_forecast["main"]["temp"] - 273.15
    hum = client.full_weather_forecast["main"]["humidity"]
    wind_speed = client.full_weather_forecast["wind"]["speed"]
    wind_direction = client.full_weather_forecast["wind"]["deg"]
    print(f"The current temperature in {city} is {temp:.1f} °C.")
    print(f"The current humidity in {city} is {hum}%.")
    print(
        f"The current wind speed in {city} is {wind_speed} m/s from direction {wind_direction} degrees."
    )


if __name__ == "__main__":
    main()
