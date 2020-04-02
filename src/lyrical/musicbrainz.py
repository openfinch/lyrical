# src/lyrical/musicbrainz.py
"""Client for the Musicbrainz REST API."""
from dataclasses import dataclass

import click
import desert
import marshmallow
import requests

from . import __version__

USER_AGENT: str = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL: str = "https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"


@dataclass
class Artist:
    """Artist resource.

    Attributes:
        id: Unique id of artist in Musicbrainz.
        name: Name of the artist.
        sort_name: Sort-alphabetised name of the artist.
        established: Year the artist was established.
        hometown: Hometown of the artist.
        country: Home country of the artist.
    """

    id: str
    name: str
    sort_name: str
    established: str
    hometown: str
    country: str = "Unknown"


artist_schema = desert.schema(Artist, meta={"unknown": marshmallow.EXCLUDE})


def search(name: str) -> Artist:
    """Search for an artist.

    Performs a GET request to the /artist/?query={query} endpoint.

    Args:
        name: The url-encoded name of the artist

    Returns:
        An Artist resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    Example:
        >>> from lyrical import musicbrainz
        >>> artist = musicbrainz.search(name="The%20Cure")
        >>> artist.name
        "The Cure"
    """
    try:
        with requests.get(
            SEARCH_API_URL.format(query=name), headers={"User-Agent": USER_AGENT}
        ) as response:
            response.raise_for_status()
            data = response.json()

            # Normalise search response taking top result
            data = data["artists"][0]
            data["sort_name"] = data.pop("sort-name")
            hometown = (
                data.pop("begin-area") if "begin-area" in data else {"name": "Unknown"}
            )
            lifespan = (
                data.pop("life-span")
                if "begin" in data["life-span"]
                else {"begin": "Unknown"}
            )
            data["hometown"] = hometown["name"]
            data["established"] = lifespan["begin"]

            return artist_schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message: str = str(error)
        raise click.ClickException(message)
