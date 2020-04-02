# src/lyrical/console.py
import textwrap
from urllib.parse import quote

import click

from . import __version__, musicbrainz

USER_AGENT = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL = "https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """Lyrical, the lyric analysis python tool."""
    pass  # pragma: no cover


@main.command("search", short_help="Search the Musicbrainz database by artist.")
@click.option("--name", prompt="Artist Name", help="The artist to search for")
def search(name: str) -> None:
    data = musicbrainz.search(quote(name))

    extract: str = f"{data.name}, {data.established} ({data.hometown}, {data.country})"

    click.secho(data.name, fg="green")
    click.echo(textwrap.fill(extract))
