import pytest

from gptravel.core.services.geocoder import GeoCoder
from gptravel.core.services.scorer import (
    CitiesCountryScorer,
    DayGenerationScorer,
    TravelPlanScore,
)


@pytest.fixture(autouse=True)
def geo_coder() -> GeoCoder:
    return GeoCoder()


@pytest.fixture
def score_container() -> TravelPlanScore:
    return TravelPlanScore()


@pytest.fixture
def cities_country_scorer(geo_coder: GeoCoder) -> CitiesCountryScorer:
    return CitiesCountryScorer(geo_coder)


@pytest.fixture
def day_generation_scorer() -> DayGenerationScorer:
    return DayGenerationScorer()
