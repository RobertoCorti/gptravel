import pytest

from gptravel.core.utils.regex_tool import JsonExtractor


@pytest.fixture
def extractor() -> JsonExtractor:
    return JsonExtractor()
