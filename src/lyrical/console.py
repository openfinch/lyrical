# src/hypermodern_python/console.py
import json
import textwrap
from urllib.parse import quote

import click
import requests

from . import __version__

USER_AGENT = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL="https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"


@click.group()
@click.version_option(version=__version__)
def main():
    """Lyrical, the lyric analysis python tool."""
    pass

@main.command('search', short_help="Search the Musicbrainz database by artist.")
@click.option('--name', prompt='Artist Name', help='The artist to search for')
def search(name):
    with requests.get(SEARCH_API_URL.format(query=quote(name, safe=''))) as response:
        response.raise_for_status()
        data = response.json()
        
        title = data['artists'][0]['name']
        extract = f"{title}, {data['artists'][0]['life-span']['begin']} ({data['artists'][0]['begin-area']['name']}, {data['artists'][0]['country']})"
    
        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))
