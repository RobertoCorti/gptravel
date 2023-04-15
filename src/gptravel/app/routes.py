from flask import render_template, request, redirect, url_for
import pycountry

from src.gptravel.app import utils
from src.gptravel.app.geo import geolocator
from src.gptravel.app import app


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        travel_plan_args = {
            'departure': request.form['from'],
            'destination': request.form['to'],
            'departure_date': request.form['departure-date'],
            'return_date': request.form['return-date'],
            'travel_option': request.form.get('travel_option', 'None')
        }

        return redirect(url_for('travel_plan',
                                **travel_plan_args))
    else:
        return render_template('index.html')


@app.route('/from=<departure>/to=<destination>/departure_date=<departure_date>/return_date=<return_date>/travel_option=<travel_option>')
def travel_plan(departure, destination, departure_date, return_date, travel_option):
    try:
        destination_country_name = pycountry.countries.get(alpha_2=destination).name
    except AttributeError:
        destination_country_name = destination

    wiki_summary = utils.get_wikipedia_summary(destination_country_name)

    destination_coordinates = geolocator.geocode(destination_country_name).latitude, geolocator.geocode(destination_country_name).longitude

    travel_plan_json = utils.get_travel_plan()
    markers_coordinates = utils.get_travel_cities_coordinates(travel_plan_json, geolocator)
    travel_images_url = utils.get_travel_cities_images_url(travel_plan_json)

    travel_dict = {
        day: {
            city: {
                'activities': travel_plan_json[day][city],
                'coordinates': markers_coordinates[day][city],
                'image_url': travel_images_url[day][city]
            }
            for city in travel_plan_json[day].keys()
        }
        for day in travel_plan_json.keys()
    }

    return render_template(
        'travel_plan.html',
        destination=destination_country_name,
        departure_date=departure_date,
        return_date=return_date,
        summary=wiki_summary,
        destination_coordinates=destination_coordinates,
        travel_dict=travel_dict
    )


@app.route('/about')
def about():
    return render_template('about.html')
