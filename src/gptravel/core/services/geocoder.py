from functools import partial
from typing import Optional

from geopy.geocoders import Nominatim


class GeoCoder:
    def __init__(self, language: str = "en") -> None:
        self._geocoder = partial(
            Nominatim(user_agent="geoapiExercises").geocode,
            language=language,
            addressdetails=True,
        )

    def country_from_location_name(self, location_name: str) -> Optional[str]:
        try:
            return self._geocoder(location_name).raw["address"]["country"]
        except AttributeError:
            return None