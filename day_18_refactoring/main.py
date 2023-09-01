import argparse
from enum import StrEnum, auto
from typing import Any
import json
from weather import (
    get_complete_forecast,
    http_get,
    get_temperature,
    get_humidity,
    get_wind_speed,
    get_wind_direction,
)


class Condition(StrEnum):
    TEMPERATURE = auto()
    HUMIDITY = auto()
    WIND = auto()


def construct_parser(texts: dict[str, Any]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=texts["cli_description"])
    parser.add_argument("city", help=texts["help_city"])
    parser.add_argument(
        "-c",
        "--condition",
        dest="condition",
        metavar="CONDITION",
        default="temperature",
        choices=texts["conditions_all"]
        + texts["conditions_temperature"]
        + texts["conditions_humidity"]
        + texts["conditions_wind"],
        help=texts["help_condition"],
    )

    parser.add_argument(
        "--api-key",
        default="123456789",
        help=texts["help_api_key"],
    )

    return parser


def fetch_conditions_from_args(
    arg_condition: str, texts: dict[str, Any]
) -> list[Condition]:
    if arg_condition in texts["conditions_humidity"]:
        return [Condition.HUMIDITY]
    elif arg_condition in texts["conditions_wind"]:
        return [Condition.WIND]
    elif arg_condition in texts["conditions_all"]:
        return [Condition.TEMPERATURE, Condition.HUMIDITY, Condition.WIND]
    else:
        return [Condition.TEMPERATURE]


def main() -> None:
    with open("texts_de.json", "r", encoding="utf-8") as f:
        texts = json.load(f)

    parser = construct_parser(texts)
    args = parser.parse_args()

    weather_forecast = get_complete_forecast(
        http_get_fn=http_get, api_key=args.api_key, city=args.city
    )

    if weather_forecast:

        def print_condition(cond: Condition) -> None:
            info = {
                "city": args.city,
                "temperature": get_temperature(weather_forecast),
                "humidity": get_humidity(weather_forecast),
                "wind_speed": get_wind_speed(weather_forecast),
                "wind_direction": get_wind_direction(weather_forecast),
            }
            print(texts[f"info_{cond.name.lower()}"].format(**info))

        conditions = fetch_conditions_from_args(args.condition, texts)
        for condition in conditions:
            print_condition(condition)

    else:
        print(texts["error_no_data"].format(city=args.city))


if __name__ == "__main__":
    main()
