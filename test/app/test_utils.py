import unittest
from gptravel.app.geo import user_agent
from gptravel.app.utils import get_wikipedia_summary, get_travel_cities_coordinates, \
    get_travel_plan
from geopy.geocoders import Nominatim


class TestUtils(unittest.TestCase):
    def test_get_wikipedia_summary(self):
        # Test with an existing page
        self.assertEqual(
            get_wikipedia_summary("Rome"),
            "Rome (Italian and Latin: Roma [ˈroːma] (listen)) is the capital city of Italy. It is also the capital of the Lazio region, the centre of the Metropolitan City of Rome, and a special comune named Comune di Roma Capitale. With 2,860,009 residents in 1,285 km2 (496")

        # Test with a non-existing page
        self.assertIsNone(get_wikipedia_summary("This page does not exist"))

    def test_get_travel_cities_coordinates(self):
        geolocator = Nominatim(user_agent=user_agent)

        travel_plan_dict = get_travel_plan()
        expected_coords = {
            "Day 1": {
                "Rome": [41.8933203, 12.4829321],
            },
            "Day 2": {
                "Florence": [43.7698712, 11.2555757]
            }
        }
        self.assertDictEqual(get_travel_cities_coordinates(travel_plan_dict, geolocator), expected_coords)


if __name__ == '__main__':
    unittest.main()
