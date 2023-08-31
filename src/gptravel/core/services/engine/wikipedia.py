from abc import ABC
from typing import Optional

from wikipediaapi import Wikipedia, WikipediaPage

from gptravel.core.services.geocoder import GeoCoder


class WikipediaEngine(ABC):
    def __init__(self) -> None:
        self._wiki_wiki = Wikipedia("Gptravel project", "en")

    def _page(self, title_page: str) -> WikipediaPage:
        return self._wiki_wiki.page(title=title_page)

    @property
    def url(self) -> Optional[str]:
        return self._page.fullurl


class WikipediaPlaces(WikipediaEngine):
    def __init__(self, geodecoder: GeoCoder) -> None:
        super().__init__()
        self._geopy = geodecoder

    @property
    def url(self) -> Optional[str]:
        city = self._geodecoder
        return super().url
