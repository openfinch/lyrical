"""Analysis library for lyrics corpuses."""
from dataclasses import dataclass
import statistics
from typing import List

import click
import desert
import marshmallow

from .ovh import LyricsCorpus


@dataclass
class TokenisedCorpus:
    """TokenisedCorpus resource.

    Attributes:
        title: Title of the track
        artist: Name of the artist
        tokens: lyrics of the track as a list of words
    """

    title: str
    artist: str
    tokens: List[str]


tokens_schema = desert.schema(TokenisedCorpus, meta={"unknown": marshmallow.EXCLUDE})


def tokenise(corpus: List[LyricsCorpus]) -> List[TokenisedCorpus]:
    """Tokenise a lyrics corpus.

    Breaks a LyricsCorpus into a list of words (tokens).

    Args:
        corpus: The name of the artist

    Returns:
        A TokenisedCorpus resource

    """
    click.echo("Tokenising lyrics corpus")
    words = []
    for song in corpus:
        tokens = song.lyrics.split()
        words.append(
            tokens_schema.load(
                {"title": song.title, "artist": song.artist, "tokens": tokens}
            )
        )

    return words


def wordcount(corpus: List[TokenisedCorpus]) -> None:
    """Calculate wordcounts for a corpus.

    Calculates the average, standard deviation and variance of
    a LyricsCorpus.

    Args:
        corpus: A list of TokenisedCorpus objects

    """
    click.echo("Analysing Wordcount of song: ")
    words = []
    for song in corpus:
        words.append(len(song.tokens))

    average = sum(words) / len(words)
    stdev = statistics.stdev(words)
    var = statistics.variance(words)

    click.echo(f"Average: {average}")
    click.echo(f"Std dev: {stdev}")
    click.echo(f"Variance: {var}")
