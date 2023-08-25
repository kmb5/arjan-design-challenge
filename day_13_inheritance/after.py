import os
from dotenv import load_dotenv


import requests


class CityNotFoundError(Exception):
    pass


class WeatherService:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def retrieve_forecast(self, city: str) -> None:
        params = {
            "q": city,
            "appid": self.api_key,
        }
        response = requests.get(self.BASE_URL, params=params, timeout=5).json()
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )

        return response

    def print_current_temperature(self, city: str) -> None:
        forecast = self.retrieve_forecast(city=city)
        if forecast:
            temp = forecast["main"]["temp"] - 273.15
            print(f"The current temperature in {city} is {temp:.1f} °C.")


class WeatherServiceCreationError(Exception):
    pass


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


if __name__ == "__main__":
    weather_service = WeatherServiceFactory.create_weather_service()
    weather_service.retrieve_forecast(city="Utrecht")
