import click
import requests

from . import __version__

USER_AGENT = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL="https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"

def search(name):
    try:
        with requests.get(SEARCH_API_URL.format(query=name),headers={'User-Agent': USER_AGENT}) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)