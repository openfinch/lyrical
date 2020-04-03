# src/lyrical/console.py
"""Command-line interface."""
import sys
import textwrap
from urllib.parse import quote

import click

from . import __version__, analyses, musicbrainz, ovh

USER_AGENT = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL = "https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Lyrical, the lyric analysis python tool."""
    pass  # pragma: no cover


@main.command("search", short_help="Search the Musicbrainz database by artist.")
@click.option("--name", prompt="Artist Name", help="The artist to search for")
@click.option(
    "--tracklist",
    is_flag=True,
    default=False,
    help="Should Lyrical fetch a tracklist for this artist?",
)
@click.option(
    "--deduplicate",
    is_flag=True,
    default=False,
    help="Should Lyrical deduplicate the tracklist?",
)
def search(name: str, tracklist: bool = False, deduplicate: bool = False) -> None:
    """Search for an artist."""
    artist = musicbrainz.search(quote(name))

    extract = (
        f"{artist.name}, {artist.established} ({artist.hometown}, {artist.country})"
    )

    click.secho(artist.id, fg="green")
    click.echo(textwrap.fill(extract))

    if tracklist:
        tracks = musicbrainz.recordings(quote(artist.id), deduplicate)
        click.echo("Track List: ")
        click.echo(tracks.recordings)


@main.command("analyse", short_help="Analyse a lyrics corpus for a given artist.")
@click.option("--name", prompt="Artist Name", help="The artist to search for")
@click.option(
    "--analysis",
    help="Which analysis should Lyrical run? {all, wordcount}",
    default="all",
)
@click.option(
    "--deduplicate",
    is_flag=True,
    default=False,
    help="Should Lyrical deduplicate the tracklist?",
)
def analyse(name: str, analysis: str = "all", deduplicate: bool = False) -> None:
    """Search for an artist."""
    if analysis not in ("all", "wordcount"):
        click.secho(
            "Analysis not recognised, valid options are {all, wordcount}", fg="red"
        )
        sys.exit(1)

    click.echo("Fetching artist from Musicbrainz")
    artist = musicbrainz.search(quote(name))

    extract: str = f"{artist.name}, {artist.established} ({artist.hometown}, {artist.country})"

    click.secho(artist.id, fg="green")
    click.echo(textwrap.fill(extract))

    click.echo("Fetching recordings from Musicbrainz")
    tracklist = musicbrainz.recordings(quote(artist.id), deduplicate)

    click.echo("Generating corpus from lyrics.ovh")
    lyric_corpus = ovh.build_corpus(artist.name, tracklist.recordings)

    if analysis == "all" or analysis == "wordcount":
        tokenised_corpus = analyses.tokenise(lyric_corpus)
        analyses.wordcount(tokenised_corpus)
