from main import fetch_conditions_from_args, Condition


def test_fetch_conditions_from_args() -> None:
    texts = {
        "conditions_temperature": ["temperature", "t"],
        "conditions_wind": ["wind", "w"],
        "conditions_humidity": ["humidity", "h"],
        "conditions_all": ["all", "a"],
    }

    # Test temperature condition
    assert fetch_conditions_from_args("temperature", texts) == [Condition.TEMPERATURE]
    assert fetch_conditions_from_args("t", texts) == [Condition.TEMPERATURE]

    # Test wind condition
    assert fetch_conditions_from_args("wind", texts) == [Condition.WIND]
    assert fetch_conditions_from_args("w", texts) == [Condition.WIND]

    # Test humidity condition
    assert fetch_conditions_from_args("humidity", texts) == [Condition.HUMIDITY]
    assert fetch_conditions_from_args("h", texts) == [Condition.HUMIDITY]

    # Test all conditions
    assert fetch_conditions_from_args("all", texts) == [
        Condition.TEMPERATURE,
        Condition.HUMIDITY,
        Condition.WIND,
    ]
    assert fetch_conditions_from_args("a", texts) == [
        Condition.TEMPERATURE,
        Condition.HUMIDITY,
        Condition.WIND,
    ]

    # Test unknown condition
    assert fetch_conditions_from_args("unknown", texts) == [Condition.TEMPERATURE]
