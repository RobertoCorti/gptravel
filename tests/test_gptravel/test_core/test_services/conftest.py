import pytest

from gptravel.core.services.geocoder import Geocoder
from gptravel.core.services.scorer import (
    CitiesCountryScorer,
    DayGenerationScorer,
    OptimizedItineraryScorer,
    TravelPlanScore,
)


@pytest.fixture(autouse=True)
def geo_coder() -> Geocoder:
    return Geocoder(
        language="en",
        min_delay_seconds=3,
        error_wait_seconds=10,
        max_retries=4,
    )


@pytest.fixture
def score_container() -> TravelPlanScore:
    return TravelPlanScore()


@pytest.fixture
def cities_country_scorer(geo_coder: Geocoder) -> CitiesCountryScorer:
    return CitiesCountryScorer(geo_coder)


@pytest.fixture
def day_generation_scorer() -> DayGenerationScorer:
    return DayGenerationScorer()


@pytest.fixture
def itinerary_scorer(geo_coder: Geocoder) -> OptimizedItineraryScorer:
    return OptimizedItineraryScorer(geo_coder)
