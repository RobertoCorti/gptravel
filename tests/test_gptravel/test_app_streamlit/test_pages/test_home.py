import datetime
import os

import dotenv
import pytest

from gptravel.prototype.pages import home

dotenv.load_dotenv()


@pytest.fixture
def departure_date():
    return datetime.datetime(2023, 6, 15)


@pytest.fixture
def return_date():
    return datetime.datetime(2023, 6, 20)


@pytest.fixture
def openai_key():
    return os.environ.get("OPENAI_API_KEY")


@pytest.fixture
def departure_place():
    return "Milan"


@pytest.fixture
def destination_place():
    return "New York"


@pytest.mark.parametrize(
    "departure, destination",
    [
        ("Milan", "India"),
        ("New York", "Italy"),
        ("Japan", "United States"),
    ],
)
def test_is_valid_input_correct(
    departure, destination, departure_date, return_date, openai_key
):
    assert home._is_valid_input(
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        openai_key=openai_key,
    )


def test_is_valid_input_wrong_dates(departure_place, destination_place, openai_key):
    departure_date = datetime.date(2023, 1, 1)
    return_date = datetime.date(2022, 11, 1)

    assert not home._is_valid_input(
        departure=departure_place,
        destination=destination_place,
        departure_date=departure_date,
        return_date=return_date,
        openai_key=openai_key,
    )


@pytest.mark.parametrize(
    "departure, destination",
    [
        ("Milan", "Pippo"),
        ("New York", "Pluto"),
    ],
)
def test_is_valid_input_wrong_places(
    departure, destination, departure_date, return_date, openai_key
):
    assert not home._is_valid_input(
        departure=departure,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        openai_key=openai_key,
    )


def test_is_valid_input_wrong_openai_key(
    departure_place, destination_place, departure_date, return_date, openai_key
):
    assert not home._is_valid_input(
        departure=departure_place,
        destination=destination_place,
        departure_date=departure_date,
        return_date=return_date,
        openai_key="a",
    )
