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
        output = geo_coder.location_coordinates("delhi")
        assert output["lat"] == pytest.approx(28.6, 0.1)
        assert output["lon"] == pytest.approx(77.2, 0.1)
        assert geo_coder.location_coordinates("PortaSigrar") == {
            "lat": None,
            "lon": None,
        }

    def test_location_distance(self, geo_coder: GeoCoder):
        assert geo_coder.location_distance("kolkata", "delhi") == pytest.approx(
            1305.106, 0.001
        )
        assert geo_coder.location_distance("delhi", "delhi") == pytest.approx(
            0.0, 0.001
        )

    @pytest.mark.parametrize(
        "location_name, expected_result",
        [
            ("United States", True),
            ("California", True),
            ("New York", True),
            ("Italy", True),
            ("Rome", True),
            ("Berlin", True),
            ("Milan", True),
            ("Pippo", False),
        ],
    )
    def test_is_location_country_city_state(
        self, geo_coder, location_name, expected_result
    ):
        assert (
            geo_coder.is_location_country_city_state(location_name) == expected_result
        )

    @pytest.mark.parametrize(
        "location_name, expected_result",
        [
            ("United States", True),
            ("California", True),
            ("New York", False),
            ("Italy", True),
            ("Rome", False),
            ("Berlin", False),
            ("Milan", False),
            ("Pippo", False),
        ],
    )
    def test_is_location_country(self, geo_coder, location_name, expected_result):
        assert geo_coder.is_a_country(location_name) == expected_result
