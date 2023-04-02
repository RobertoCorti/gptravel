import pytest

from gptravel.core.services.geocoder import GeoCoder


class TestGeoCoder:
    def test_country_from_location_name(self, geo_coder: GeoCoder):
        assert geo_coder.country_from_location_name("Paris, France") == "France"
        assert geo_coder.country_from_location_name("London, UK") == "United Kingdom"
        assert (
            geo_coder.country_from_location_name("Los Angeles, US") == "United States"
        )
        assert geo_coder.country_from_location_name("Mumbai, India") == "India"
        assert geo_coder.country_from_location_name("PortaSigrar") is None
