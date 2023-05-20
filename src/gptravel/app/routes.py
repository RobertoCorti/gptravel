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

MAX_TOKENS = 1024


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
    n_days = (
            datetime.datetime.strptime(return_date, '%Y-%m-%d') - datetime.datetime.strptime(departure_date, '%Y-%m-%d')
    ).days

    try:
        departure_country_name = pycountry.countries.get(alpha_2=departure).name
        destination_country_name = pycountry.countries.get(alpha_2=destination).name
    except AttributeError:
        destination_country_name = destination
        departure_country_name = departure

    travel_parameters = {
        "departure_place": departure_country_name,
        "destination_place": destination_country_name,
        "n_travel_days": n_days,
        "travel_theme": travel_option
    }

    prompt_factory = PromptFactory()
    prompt = prompt_factory.build_prompt(**travel_parameters)
    engine = openai_engine.ChatGPTravelEngine(max_tokens=MAX_TOKENS)

    #travel_plan_json = engine.get_travel_plan_json(prompt).travel_plan
    travel_plan_json = mock_get_travel_plan_json()

    """
    zs_classifier = classifier.ZeroShotTextClassifier(True)
    geo_decoder = geocoder.GeoCoder()
    score_container = scorer.TravelPlanScore()
    scorers_orchestrator = score_builder.ScorerOrchestrator(
        geocoder=geo_decoder, text_classifier=zs_classifier
    )
    scorers_orchestrator.run(
        travel_plan_json=travel_plan_json, scores_container=score_container
    )
    score = round(score_container.weighted_score*10, 2)
    """
    score = 8.5
    travel_score_description = utils.get_score_description(score)
    destination_coordinates = geolocator.geocode(destination).latitude, geolocator.geocode(destination).longitude
    markers_coordinates = utils.get_travel_cities_coordinates(travel_plan_json, geolocator)
    travel_dict = {
        day: {
            city: {
                'activities': travel_plan_json[day][city],
                'coordinates': markers_coordinates[day][city],
            }
            for city in travel_plan_json[day].keys()
        }
        for day in travel_plan_json.keys()
    }


    return render_template(
        'travel_plan.html',
        departure=departure_country_name,
        destination=destination_country_name,
        departure_date=departure_date,
        return_date=return_date,
        travel_plan_json=travel_plan_json,
        travel_score_description=travel_score_description,
        travel_score=score,
        destination_coordinates=destination_coordinates,
        markers_coordinates=markers_coordinates,
        travel_dict=travel_dict,
    )



@app.route('/about')
def about():
    return render_template('about.html')
