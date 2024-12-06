from functools import partial
from typing import Dict, List, Optional

from geopy import Location
from geopy.distance import geodesic as GRC
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Photon

from gptravel.core.io.loggerconfig import logger

LOCATION_CACHE: Dict[str, Location] = {}


class Geocoder:
    def __init__(
        self,
        language: str = "en",
        min_delay_seconds: int = 0,
        error_wait_seconds: int = 7,
        max_retries: int = 3,
    ) -> None:
        self._geocoder = partial(
            RateLimiter(
                Photon().geocode,
                min_delay_seconds=min_delay_seconds,
                max_retries=max_retries,
                error_wait_seconds=error_wait_seconds,
            ),
            language=language,
        )

    def _query(self, location_name: str) -> Optional[Location]:
        loc_name = location_name.lower()
        logger.debug("Querying coordinates for %s", loc_name)
        if loc_name in LOCATION_CACHE:
            logger.debug("Using cached coordinates")
            return LOCATION_CACHE[loc_name]
        logger.debug("Downloading new Location for %s: Start", loc_name)
        qry_obj = self._geocoder(location_name)
        logger.debug("Downloading new Location for %s: Complete", loc_name)
        LOCATION_CACHE[loc_name] = qry_obj
        return qry_obj

    def _location_type(self, location_name: str) -> Optional[List[str]]:
        fetched_location = self._query(location_name)
        location_type = None
        if fetched_location is not None:
            location_type = fetched_location.raw["properties"]["type"]
        logger.debug("GeoCoder: type for %s is: %s", location_name, location_type)
        return location_type

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

    def location_distance(
        self, location_name_1: str, location_name_2: str
    ) -> Optional[float]:
        if location_name_1.lower() == location_name_2.lower():
            return 0.0
        location1_coords = self.location_coordinates(location_name_1)
        location2_coords = self.location_coordinates(location_name_2)
        if (location1_coords["lat"] is not None) & (
            location2_coords["lat"] is not None
        ):
            return GRC(
                (location1_coords["lat"], location1_coords["lon"]),
                (location2_coords["lat"], location2_coords["lon"]),
            ).km
        return None

    def is_location_country_city_state(self, location_name: str) -> bool:
        location_type = self._location_type(location_name)
        if location_type:
            return location_type in ["country", "state", "city"]
        return False

    def is_a_country(self, location_name: str) -> bool:
        location_type = self._location_type(location_name)
        if location_type:
            return location_type in ["country", "state"]
        return False
