from typing import Optional

from wikipediaapi import Wikipedia, WikipediaPage


class WikipediaEngine:
    def __init__(self) -> None:
        self._wiki_wiki = Wikipedia("Gptravel project", "en")

    def _page(self, title_page: str) -> WikipediaPage:
        return self._wiki_wiki.page(title=title_page)

    def url(self, title_page: str) -> Optional[str]:
        try:
            return self._page(title_page).fullurl
        except KeyError:
            return None
