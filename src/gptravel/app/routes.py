from flask import render_template, request, redirect, url_for
import pycountry

from src.gptravel.app import utils
from src.gptravel.app.geo import geolocator
from src.gptravel.app import app


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
    wiki_summary = utils.get_wikipedia_summary(destination)

    destination_coordinates = geolocator.geocode(destination).latitude, geolocator.geocode(destination).longitude

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
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        summary=wiki_summary,
        destination_coordinates=destination_coordinates,
        travel_dict=travel_dict
    )


@app.route('/about')
def about():
    return render_template('about.html')
