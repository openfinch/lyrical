# tests/test_musicbrainz.py
import click
import pytest

from lyrical import musicbrainz


def test_artist_search_returns_at_least_one_result():
    data = musicbrainz.search(name="The Cure")
    assert "artists" in data
    assert len(data["artists"]) > 0


def test_artist_search_returns_correct_result_simple():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="The Cure")
    assert "artists" in data
    assert data["artists"][0]["name"] == "The Cure"


def test_artist_search_returns_correct_result_escapes():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="Sunn O)))")
    assert "artists" in data
    assert data["artists"][0]["name"] == "Sunn O)))"


def test_artist_search_returns_correct_result_unicode():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="兀突骨")
    assert "artists" in data
    assert data["artists"][0]["name"] == "兀突骨"


def test_artist_search_returns_correct_result_unicode2():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.

    data = musicbrainz.search(name="ℑ⊇≥◊≤⊆ℜ")  # Yes, this is a real band
    assert "artists" in data
    assert data["artists"][0]["name"] == "ℑ⊇≥◊≤⊆ℜ"


def test_artist_search_returns_exception_on_error():
    # REVIEW: This one is a bit fuzzy, definitely one to revisit.
    with pytest.raises(click.exceptions.ClickException):
        musicbrainz.search(name="")
