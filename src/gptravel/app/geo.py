import os
from geopy.geocoders import Nominatim

user_agent = os.environ.get("GEOPY_USER_AGENT", "GPTravel")

geolocator = Nominatim(user_agent=user_agent)
