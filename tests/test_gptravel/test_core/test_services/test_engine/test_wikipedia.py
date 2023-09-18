import pytest
from wikipediaapi import WikipediaPage

from gptravel.core.services.engine.wikipedia import WikipediaEngine


class TestWikipediaEngine:
    @pytest.fixture
    def wikipedia_engine(self) -> WikipediaEngine:
        return WikipediaEngine()

    def test_url_valid_title(self, wikipedia_engine: WikipediaEngine):
        title = "Python (programming language)"
        url = wikipedia_engine.url(title)
        assert url is not None
        assert isinstance(url, str)
        assert "wikipedia.org" in url

    def test_url_invalid_title(self, wikipedia_engine: WikipediaEngine):
        title = "Invalid Title"
        url = wikipedia_engine.url(title)
        assert url is None

    def test_page_exists(self, wikipedia_engine: WikipediaEngine):
        title = "Python (programming language)"
        page = wikipedia_engine._page(title)
        assert isinstance(page, WikipediaPage)
        assert page.exists()

    def test_page_not_exists(self, wikipedia_engine: WikipediaEngine):
        title = "Invalid Title"
        page = wikipedia_engine._page(title)
        assert isinstance(page, WikipediaPage)
        assert not page.exists()
