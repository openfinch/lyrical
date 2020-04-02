# tests/test_musicbrainz.py
import click
import pytest

from lyrical import musicbrainz


def test_artist_search_returns_correct_result_simple():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="The Cure")
    assert data.name == "The Cure"


def test_artist_search_returns_correct_result_escapes():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="Sunn O)))")
    assert data.name == "Sunn O)))"


def test_artist_search_returns_correct_result_unicode():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="兀突骨")
    assert data.name == "兀突骨"


def test_artist_search_returns_correct_result_unicode2():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="ℑ⊇≥◊≤⊆ℜ")  # Yes, this is a real band
    assert data.name == "ℑ⊇≥◊≤⊆ℜ"


def test_artist_search_returns_exception_on_error():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.
    with pytest.raises(click.exceptions.ClickException):
        musicbrainz.search(name="")
