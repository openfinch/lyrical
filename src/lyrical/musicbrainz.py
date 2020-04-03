# src/lyrical/musicbrainz.py
"""Client for the Musicbrainz REST API."""
from concurrent.futures import as_completed
from dataclasses import dataclass
from typing import List

import click
import desert
import marshmallow
import requests
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3.util.retry import Retry

from . import __version__


USER_AGENT: str = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
SEARCH_API_URL: str = "https://musicbrainz.org/ws/2/artist/?query={query}&fmt=json"
RELEASES_API_URL: str = "https://musicbrainz.org/ws/2/recording?artist={id}&limit={limit}&offset={offset}&fmt=json"


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


@dataclass
class Recordings:
    """Recordings resource.

    Attributes:
        recordings: List of recordings
    """

    recordings: List[str]


recordings_schema = desert.schema(Recordings, meta={"unknown": marshmallow.EXCLUDE})


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


def recordings(id: str, deduplicate: bool) -> Recordings:
    """Search for an artist.

    Performs a GET request to the /recording?query=arid:{id} endpoint.

    Args:
        id: The unique id of the artist
        deduplicate: Whether the recording list should be deduplicated

    Returns:
        A list of Recording resources

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    """
    try:
        count = 0
        limit = 100
        offset = 0
        recordings = []
        errors = []
        urls = []
        batch_size = 1

        # Generate a list of URLs to call with grequest
        with requests.get(
            RELEASES_API_URL.format(id=id, limit=1, offset=0),
            headers={"User-Agent": USER_AGENT},
        ) as response:
            response.raise_for_status()
            count = response.json()["recording-count"]

            # Generate a list of pages for official releases
            while count > offset:
                urls.append(RELEASES_API_URL.format(id=id, limit=limit, offset=offset))
                offset += limit

        # Generate and iterate over a set of request futures
        with FuturesSession(max_workers=batch_size) as session:
            retries = 5
            status_forcelist = [503]
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                respect_retry_after_header=True,
                backoff_factor=1,
                status_forcelist=status_forcelist,
            )

            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)

            futures = [
                session.get(url, headers={"User-Agent": USER_AGENT}) for url in urls
            ]

            for future in as_completed(futures):
                resp = future.result()
                resp_json = resp.json()
                if resp.status_code != 200:
                    errors.append(resp_json)
                else:
                    for recording in resp_json["recordings"]:
                        recordings.append(recording["title"])

        # This is slow, but gets nicer results
        if deduplicate:
            recordings = list(set(recordings))

        return recordings_schema.load({"recordings": recordings})

    except (requests.RequestException, marshmallow.ValidationError) as error:
        message: str = str(error)
        raise click.ClickException(message)
