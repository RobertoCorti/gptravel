from typing import Dict, Optional

import pytest

from gptravel.core.services.geocoder import Geocoder


class TestGeoCoder:
    @pytest.mark.parametrize(
        "location_name, expected_country",
        [
            ("Paris, France", "France"),
            ("London, UK", "United Kingdom"),
            ("Los Angelese, US", "United States"),
            ("Mumbay, India", "India"),
            ("PortaSigrar", None),
        ],
    )
    def test_country_from_location_name(
        self, geo_coder: Geocoder, location_name: str, expected_country: Optional[str]
    ):
        assert geo_coder.country_from_location_name(location_name) == expected_country

    @pytest.mark.parametrize(
        "location_name, expected_coordinates",
        [
            ("kolkata", {"lat": 22.9, "lon": 88.4}),
            ("delhi", {"lat": 28.6, "lon": 77.2}),
            ("PortaSigrar", {"lat": None, "lon": None}),
        ],
    )
    def test_location_coordinates(
        self,
        geo_coder: Geocoder,
        location_name: str,
        expected_coordinates: Dict[str, Optional[float]],
    ):
        coords = geo_coder.location_coordinates(location_name)
        keys = ["lat", "lon"]
        for k in keys:
            assert coords[k] == pytest.approx(expected_coordinates[k], 0.1)

    @pytest.mark.parametrize(
        "location1, location2, expected_distance",
        [
            ("kolkata", "delhi", 1305.106),
            ("delhi", "delhi", 0.0),
            ("PortaSigrar", "delhi", None),
        ],
    )
    def test_location_distance(
        self,
        geo_coder: Geocoder,
        location1: str,
        location2: str,
        expected_distance: float,
    ):
        assert geo_coder.location_distance(location1, location2) == pytest.approx(
            expected_distance, 0.001
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
        self, geo_coder: Geocoder, location_name: str, expected_result: bool
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
    def test_is_location_country(
        self, geo_coder: Geocoder, location_name: str, expected_result: bool
    ):
        assert geo_coder.is_a_country(location_name) == expected_result
