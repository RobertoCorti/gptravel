from gptravel.core.services.engine.classifier import TextClassifier
from gptravel.core.services.engine.entity_recognizer import EntityRecognizer
from gptravel.core.services.geocoder import Geocoder
from gptravel.core.services.scorer import (
    ActivitiesDiversityScorer,
    ActivityPlacesScorer,
    CitiesCountryScorer,
    DayGenerationScorer,
    OptimizedItineraryScorer,
    TravelPlanScore,
)
from gptravel.core.travel_planner.travel_engine import TravelPlanJSON


class ScorerOrchestrator:
    def __init__(self, geocoder: Geocoder, text_classifier: TextClassifier) -> None:
        self._scorers = [
            ActivitiesDiversityScorer(text_classifier),
            ActivityPlacesScorer(
                geolocator=geocoder, entity_recognizer=EntityRecognizer()
            ),
            DayGenerationScorer(),
            CitiesCountryScorer(geolocator=geocoder),
            OptimizedItineraryScorer(geolocator=geocoder),
        ]

    def run(
        self, travel_plan_json: TravelPlanJSON, scores_container: TravelPlanScore
    ) -> None:
        for scorer in self._scorers:
            scorer.score(
                travel_plan=travel_plan_json, travel_plan_scores=scores_container
            )
