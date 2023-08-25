from enum import Enum
import pandas as pd
from typing import Any


class FilterOption(Enum):
    ALL = "All"
    TEMPERATURE = "Temperature"
    HUMIDITY = "Humidity"
    CO2 = "CO2"

    def __str__(self):
        return self.value


def main() -> None:
    option = FilterOption.ALL  # choose between "All", "Temperature", "Humidity", "CO2"

    data = import_data("sensor_data.csv")  # type: ignore

    filtered = filter_to_option(data, option)

    processed_data = process_data(filtered)
    print(processed_data)


def import_data(file_name: str) -> pd.DataFrame:
    data: pd.DataFrame = pd.read_csv(file_name)  # type: ignore
    return data


def filter_to_option(data: pd.DataFrame, option: FilterOption):
    if option != FilterOption.ALL:
        data = data.loc[data["Sensor"] == option.value]

    return data


def convert_to_kelvin(value: float) -> float:
    return value + 273.15


def convert_to_scale(value: float) -> float:
    return value / 100


def compensate_bias(value: float) -> float:
    return value + 23


def treat_row(row: "pd.Series[Any]") -> float:
    sensor = row["Sensor"]
    if sensor == "Temperature":
        return convert_to_kelvin(row["Value"])
    elif sensor == "Humidity":
        return convert_to_scale(row["Value"])
    elif sensor == "CO2":
        return compensate_bias(row["Value"])
    return row["Value"]


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    processed_data = data.copy()
    processed_data["Value"] = processed_data.apply(treat_row, axis=1)  # type: ignore

    return processed_data


if __name__ == "__main__":
    main()
