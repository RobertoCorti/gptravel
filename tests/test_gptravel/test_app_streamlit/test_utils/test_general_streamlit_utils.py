import os
import pytest
import openai
import datetime

from gptravel.prototype.utils import is_valid_location, is_valid_openai_key, is_departure_before_return


@pytest.mark.parametrize("location, expected_result", [
    ('city1', False),
    ('paris', True),
    ('pippo', False),
    ('los angeles', True),
    ('China', True),
    ('ITALY', True),
])
def test_is_valid_location(location, expected_result):
    assert is_valid_location(location) == expected_result


def test_is_valid_openai_key():
    from dotenv import load_dotenv
    load_dotenv()
    valid_key = os.environ.get("OPENAI_API_KEY")
    invalid_key = "pippo"

    openai.api_key = valid_key
    assert is_valid_openai_key(valid_key) == True

    openai.api_key = invalid_key
    assert is_valid_openai_key(invalid_key) == False


@pytest.mark.parametrize("departure_date, return_date, expected_result", [
    (datetime.date(2023, 6, 1), datetime.date(2023, 6, 2), True),
    (datetime.date(2023, 6, 3), datetime.date(2023, 6, 2), False),
    (datetime.date(2023, 6, 2), datetime.date(2023, 6, 2), True),
    (datetime.date(2023, 5, 31), datetime.date(2023, 6, 2), True),
])
def test_is_departure_before_return(departure_date, return_date, expected_result):
    assert is_departure_before_return(departure_date, return_date) == expected_result
