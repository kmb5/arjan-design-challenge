from dataclasses import dataclass
from typing import Any
import requests
import asyncio
from timeit import timeit

JSON = int | str | float | bool | None | dict[str, "JSON"] | list["JSON"]
JSONObject = dict[str, JSON]
JSONList = list[JSON]


API_KEY = ""


@dataclass
class UrlTemplateClient:
    template: str

    async def get(self, data: dict[str, Any]) -> JSON:
        url = self.template.format(**data)
        return await http_get(url)


class CityNotFoundError(Exception):
    pass


def http_get_sync(url: str) -> JSON:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()


async def http_get(url: str) -> JSON:
    return await asyncio.to_thread(http_get_sync, url)


async def get_capital(country: str) -> str:
    client = UrlTemplateClient(template="https://restcountries.com/v3/name/{country}")
    response = await client.get({"country": country})

    # The API can return multiple matches, so we just return the capital of the first match
    return response[0]["capital"][0]  # type: ignore


async def get_forecast(city: str) -> JSON:
    client = UrlTemplateClient(
        template=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )
    response = await client.get({"city": city})
    if "main" not in response:  # type: ignore
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


async def get_temperature(city: str) -> float:
    full_weather_forecast = await get_forecast(city)
    return (
        full_weather_forecast["main"]["temp"] - 273.15  # type: ignore
    )  # convert from Kelvin to Celsius


async def print_capital_temperature(country: str) -> None:
    capital = await get_capital(country)
    temperature = await get_temperature(capital)
    print(f"The current temperature in {capital} ({country}) is {temperature:.1f} °C.")


async def main() -> None:
    countries = ["United States of America", "Australia", "Japan", "France", "Brazil"]

    await asyncio.gather(*[print_capital_temperature(country) for country in countries])


if __name__ == "__main__":
    print(timeit("asyncio.run(main())", globals=globals(), number=1))
