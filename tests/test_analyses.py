# tests/test_analyses.py
import io
import sys

import pytest

from lyrical import analyses
from lyrical.ovh import lyrics_schema


@pytest.fixture
def lyrics_corpus():
    lyrics = """
        Slowly fading blue
        The eastern hollows catch
        The dying sun
        Night-time follows
        Silence and black
        Mirror pool mirrors
        The lonely place
        Where I meet you
        """

    payload = {"artist": "The Cure", "title": "Fire In Cairo", "lyrics": lyrics}
    return lyrics_schema.load(payload)


@pytest.fixture
def lyrics_corpus2():
    lyrics = """
        She stands twelve feet above the flood
        She stares
        Alone
        Across the water
        """

    payload = {"artist": "The Cure", "title": "The Drowning Man", "lyrics": lyrics}
    return lyrics_schema.load(payload)


@pytest.fixture
def tokenised_corpus(lyrics_corpus, lyrics_corpus2):
    return analyses.tokenise([lyrics_corpus, lyrics_corpus2])


def test_tokeniser(lyrics_corpus):
    tokenised = analyses.tokenise([lyrics_corpus])

    assert tokenised[0].artist == "The Cure"
    assert tokenised[0].title == "Fire In Cairo"
    assert "Slowly" in tokenised[0].tokens
    assert "Slowly fading blue" not in tokenised[0].tokens


def test_wordcount(tokenised_corpus):
    captured_output = io.StringIO()
    sys.stdout = captured_output
    analyses.wordcount(tokenised_corpus)
    assert "Average" in captured_output.getvalue()
    sys.stdout = sys.__stdout__
