from functools import partial
from typing import Dict, Optional

from geopy import Location
from geopy.distance import geodesic as GRC
from geopy.geocoders import Nominatim


class GeoCoder:
    def __init__(self, language: str = "en") -> None:
        self._geocoder = partial(
            Nominatim(user_agent="geoapiExercises").geocode,
            language=language,
            addressdetails=True,
        )
        self._location_cache: Dict[str, Location] = {}

    def _query(self, location_name: str) -> Optional[Location]:
        loc_name = location_name.lower()
        if loc_name in self._location_cache:
            return self._location_cache[loc_name]
        else:
            qry_obj = self._geocoder(location_name)
            self._location_cache[loc_name] = qry_obj
        return qry_obj

    def country_from_location_name(self, location_name: str) -> Optional[str]:
        fetched_location = self._query(location_name)
        if fetched_location:
            return fetched_location.raw["address"]["country"]
        return fetched_location

    def location_coordinates(self, location_name: str) -> Dict[str, Optional[float]]:
        fetched_location = self._query(location_name)
        extraction_keys = ["lat", "lon"]
        if fetched_location:
            return dict((k, float(fetched_location.raw[k])) for k in extraction_keys)
        return {key: None for key in extraction_keys}

    def location_distance(self, location_name_1: str, location_name_2: str) -> float:
        if location_name_1.lower() == location_name_2.lower():
            return 0.0
        else:
            location1_coords = self.location_coordinates(location_name_1)
            location2_coords = self.location_coordinates(location_name_2)
            return GRC(
                (location1_coords["lat"], location1_coords["lon"]),
                (location2_coords["lat"], location2_coords["lon"]),
            ).km
