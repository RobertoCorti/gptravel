import pytest

from gptravel.prototype.utils import is_valid_location

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
