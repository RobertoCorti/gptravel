from functools import partial
from typing import Dict, Optional

from geopy import Location
from geopy.distance import geodesic as GRC
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim, Photon

LOCATION_CACHE: Dict[str, Location] = {}


class GeoCoder:
    def __init__(self, language: str = "en") -> None:
        self._geocoder = partial(
            Photon().geocode,
            language=language,
        )

    def _query(self, location_name: str) -> Optional[Location]:
        loc_name = location_name.lower()
        if loc_name in LOCATION_CACHE:
            return LOCATION_CACHE[loc_name]
        qry_obj = self._geocoder(location_name)
        LOCATION_CACHE[loc_name] = qry_obj
        return qry_obj

    def country_from_location_name(self, location_name: str) -> Optional[str]:
        fetched_location = self._query(location_name)
        if fetched_location:
            return fetched_location.raw["properties"]["country"]
        return fetched_location

    def location_coordinates(self, location_name: str) -> Dict[str, Optional[float]]:
        fetched_location = self._query(location_name)
        if fetched_location:
            return {"lat": fetched_location.latitude, "lon": fetched_location.longitude}
        return {"lat": None, "lon": None}

    def location_distance(self, location_name_1: str, location_name_2: str) -> float:
        if location_name_1.lower() == location_name_2.lower():
            return 0.0
        location1_coords = self.location_coordinates(location_name_1)
        location2_coords = self.location_coordinates(location_name_2)
        return GRC(
            (location1_coords["lat"], location1_coords["lon"]),
            (location2_coords["lat"], location2_coords["lon"]),
        ).km
