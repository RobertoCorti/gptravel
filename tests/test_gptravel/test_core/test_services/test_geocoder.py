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

    def test_location_coordinates(self, geo_coder: GeoCoder):
        assert geo_coder.location_coordinates("kolkata") == {
            "lat": 22.5726459,
            "lon": 88.3638953,
        }
        assert geo_coder.location_coordinates("delhi") == {
            "lat": 28.6517178,
            "lon": 77.2219388,
        }
        assert geo_coder.location_coordinates("PortaSigrar") == {
            "lat": None,
            "lon": None,
        }

    def test_location_distance(self, geo_coder: GeoCoder):
        assert geo_coder.location_distance("kolkata", "delhi") == pytest.approx(
            1305.106, 0.001
        )
