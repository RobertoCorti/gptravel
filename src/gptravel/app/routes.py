from flask import render_template, request, redirect, url_for
import pycountry
import wikipediaapi

from geopy.geocoders.base import Geocoder
from src.gptravel.app.geo import geolocator
from src.gptravel.app import app

wiki_wiki = wikipediaapi.Wikipedia('en')


def _get_travel_plan():
    """THIS IS HARDCODED FOR NOW, REMOVE IT"""
    return {
        "Day 1": {
            "Rome": ["Visit Colosseum", "Visit Fontana di Trevi"],
        },
        "Day 2": {
            "Florence": ["Visit Uffizi", "Walk in the city-center"]
        }
    }


def get_wikipedia_summary(destination: str) -> str:
    wiki_page = wiki_wiki.page(destination)
    wiki_summary = wiki_page.summary
    return '.'.join(wiki_summary.split('.')[:3]) if wiki_page.exists() else None


def get_markers_coordinates(travel_plan_dict: dict, geocoder: Geocoder) -> list:
    markers_coordinates = []
    for day in travel_plan_dict:
        for city in travel_plan_dict[day]:
            markers_coordinates.append([geocoder.geocode(city).latitude, geocoder.geocode(city).longitude])
    return markers_coordinates


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form['country']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        region = request.form.get('region')

        if region:
            return redirect(url_for('travel_plan',
                                    country=country,
                                    departure_date=departure_date,
                                    return_date=return_date,
                                    region=region))
        else:
            return redirect(url_for('travel_plan',
                                    country=country,
                                    departure_date=departure_date,
                                    return_date=return_date))
    else:
        return render_template('index.html')


@app.route('/travel_plan/<country>/<departure_date>/<return_date>')
@app.route('/travel_plan/<country>/<departure_date>/<return_date>/<region>')
def travel_plan(country: str, departure_date: str, return_date: str, region: str = None):
    try:
        country_name = pycountry.countries.get(alpha_2=country).name
    except AttributeError:
        country_name = country

    destination = region if region else country_name
    wiki_summary = get_wikipedia_summary(destination)

    destination_coordinates = geolocator.geocode(destination).latitude, geolocator.geocode(destination).longitude

    travel_plan_json = _get_travel_plan()

    markers_coordinates = get_markers_coordinates(travel_plan_json, geolocator)

    return render_template(
        'travel_plan.html',
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        summary=wiki_summary,
        travel_plan=travel_plan_json,
        destination_coordinates=destination_coordinates,
        markers_coordinates=markers_coordinates
    )


@app.route('/about')
def about():
    return render_template('about.html')
