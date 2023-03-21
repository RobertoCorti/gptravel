import pytest
from geopy.exc import GeocoderQueryError, GeocoderServiceError

from gptravel.core.services.geocoder import GeoCoder


@pytest.fixture
def geo_coder():
    return GeoCoder()


class TestGeoCoder:
    def test_country_from_location_name(self, geo_coder):
        assert geo_coder.country_from_location_name("Paris, France") == "France"
        assert geo_coder.country_from_location_name("London, UK") == "United Kingdom"
        assert (
            geo_coder.country_from_location_name("Los Angeles, US") == "United States"
        )
        assert geo_coder.country_from_location_name("Mumbai, India") == "India"
