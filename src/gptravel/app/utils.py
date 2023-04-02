import wikipediaapi
import requests
import json
import random
import multiprocessing
import os

from geopy.geocoders.base import Geocoder

wiki_wiki = wikipediaapi.Wikipedia('en')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')


def get_travel_plan():
    """THIS IS HARDCODED FOR NOW, REMOVE IT"""
    return {
        "Day 1": {
            "Rome": ["Visit Colosseum", "Visit Fontana di Trevi"],
        },
        "Day 2": {
            "Florence": ["Visit Uffizi", "Walk in the city-center"]
        }
    }


def get_image_from_unsplash(city: str) -> str:
    search_url = 'https://api.unsplash.com/search/photos/?query={}&orientation=landscape'.format(city)
    response = requests.get(search_url, headers={'Authorization': 'Client-ID {}'.format(UNSPLASH_ACCESS_KEY)})

    photos = json.loads(response.text)['results'] if response.status_code == 200 else []

    if len(photos) > 0:
        photo = random.choice(photos)
        image_url = photo['urls']['regular']
    else:
        image_url = None

    return image_url


def get_wikipedia_summary(destination: str) -> str:
    wiki_page = wiki_wiki.page(destination)
    wiki_summary = wiki_page.summary
    return '.'.join(wiki_summary.split('.')[:3]) if wiki_page.exists() else None


def get_travel_cities_coordinates(travel_plan_dict: dict, geocoder: Geocoder) -> dict:
    return {
        day: {
            city: [geocoder.geocode(city).latitude, geocoder.geocode(city).longitude]
            for city in day_activity.keys()
        }
        for day, day_activity in travel_plan_dict.items()
    }


def get_image_from_unsplash_pool(city: str) -> dict:
    return {city: get_image_from_unsplash(city)}


def get_travel_cities_images_url(travel_plan_dict: dict) -> dict:
    ### TODO: usare asyncio
    with multiprocessing.Pool() as pool:
        city_results_list = pool.map(get_image_from_unsplash_pool,
                                     [city for day in travel_plan_dict.values() for city in day.keys()])
        city_results = {city: image_url for city_result in city_results_list for city, image_url in city_result.items()}
        return {
            day: {
                city: city_results[city]
                for city in day_activity.keys()
            }
            for day, day_activity in travel_plan_dict.items()
        }
