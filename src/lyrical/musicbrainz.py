# src/lyrical/musicbrainz.py
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
    id: str
    name: str
    sort_name: str
    established: str
    hometown: str
    country: str = "Unknown"


artist_schema = desert.schema(Artist, meta={"unknown": marshmallow.EXCLUDE})


def search(name: str) -> Artist:
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
