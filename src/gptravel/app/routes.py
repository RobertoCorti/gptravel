import datetime
import json

from flask import render_template, request, redirect, url_for
import pycountry

from gptravel.core.services import geocoder, score_builder, scorer
from gptravel.core.services.engine import classifier
from gptravel.core.travel_planner import openai_engine
from gptravel.core.travel_planner.prompt import PromptFactory
from src.gptravel.app import utils
from src.gptravel.app.geo import geolocator
from src.gptravel.app import app
from src.gptravel.core.travel_planner.travel_engine import TravelPlanJSON
import os



def mock_get_travel_plan_json():
    with open('travel_plan_Malaysia_6.json', 'r') as f:
        travel_plan_json = json.load(f)
    return travel_plan_json


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        travel_plan_args = {
            'departure': request.form['from'],
            'destination': request.form['to'],
            'departure_date': request.form['departure-date'],
            'return_date': request.form['return-date'],
            'travel_option': request.form.get('travel-option', 'None')
        }

        return redirect(url_for('travel_plan',
                                **travel_plan_args))
    else:
        return render_template('index.html')


@app.route(
    '/from=<departure>/to=<destination>/departure_date=<departure_date>/return_date=<return_date>/travel_option=<travel_option>')
def travel_plan(departure, destination, departure_date, return_date, travel_option):
    n_days = utils.calculate_number_of_days(return_date, departure_date)

    departure_country_name, destination_country_name = utils.get_country_names(departure, destination)

    travel_parameters = utils.build_travel_parameters(departure_country_name, destination_country_name, n_days, travel_option)
    prompt = utils.build_prompt(travel_parameters)
    travel_plan_json = utils.get_travel_plan_json(prompt)
    travel_plan_dict = travel_plan_json.travel_plan

    score = utils.calculate_travel_score(travel_plan_json)
    travel_score_description = utils.get_score_description(score)

    destination_coordinates = geolocator.geocode(destination).latitude, geolocator.geocode(destination).longitude
    markers_coordinates = utils.get_travel_cities_coordinates(travel_plan_dict, geolocator)
    travel_dict = {
        day: {
            city: {
                'activities': travel_plan_dict[day][city],
                'coordinates': markers_coordinates[day][city],
            }
            for city in travel_plan_dict[day].keys()
        }
        for day in travel_plan_dict.keys()
    }

    return render_template(
        'travel_plan.html',
        departure=departure_country_name,
        destination=destination_country_name,
        departure_date=departure_date,
        return_date=return_date,
        travel_plan_json=travel_plan_dict,
        travel_score_description=travel_score_description,
        travel_score=score,
        destination_coordinates=destination_coordinates,
        markers_coordinates=markers_coordinates,
        travel_dict=travel_dict,
    )



@app.route('/about')
def about():
    return render_template('about.html')
