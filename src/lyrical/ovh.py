# src/lyrical/ovh.py
"""Client for the lyrics.ovh REST API."""
from concurrent.futures import as_completed
from dataclasses import dataclass
from typing import List
from urllib.parse import unquote, urlparse

import click
import desert
import marshmallow
import requests
from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession
from urllib3.util.retry import Retry

from . import __version__

USER_AGENT: str = f"Lyrical/{__version__} ( https://github.com/openfinch/lyrical )"
LYRICS_API_URL: str = "https://api.lyrics.ovh/v1/{artist}/{title}"


@dataclass
class LyricsCorpus:
    """LyricsCorpus resource.

    Attributes:
        title: Title of the track
        artist: Name of the artist
        lyrics: lyrics of the track
    """

    title: str
    artist: str
    lyrics: str


lyrics_schema = desert.schema(LyricsCorpus, meta={"unknown": marshmallow.EXCLUDE})


def build_corpus(artist: str, tracklist: List) -> List[LyricsCorpus]:
    """Build a lyrics corpus.

    Performs a GET request to the /recording?query=arid:{id} endpoint.

    Args:
        artist: The name of the artist
        tracklist: A list of track names

    Returns:
        A LyricsCorpus resource

    Raises:
        ClickException: The HTTP request failed or the HTTP response
            contained an invalid body.

    """
    urls = []
    batch_size = 10
    corpus = []

    try:
        # Generate a list of pages for official releases
        for track in tracklist:
            urls.append(LYRICS_API_URL.format(artist=artist, title=track))

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
                if resp.status_code == 200:
                    resp_json = resp.json()
                    url = urlparse(resp.url)
                    path = url.path.split("/")
                    if (
                        resp_json["lyrics"] != "Instrumental"
                        or len(resp_json["lyrics"]) < 0
                    ):
                        lyric = lyrics_schema.load(
                            {
                                "artist": unquote(path[2]),
                                "title": unquote(path[3]),
                                "lyrics": resp_json["lyrics"],
                            }
                        )
                        corpus.append(lyric)

        return corpus

    except (requests.RequestException, marshmallow.ValidationError) as error:
        message: str = str(error)
        raise click.ClickException(message)
