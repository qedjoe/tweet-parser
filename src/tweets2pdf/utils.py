import logging
import urllib.parse
import tempfile
from pathlib import Path
from contextlib import contextmanager

import requests
import emoji
import requests.adapters

from .settings import LANGUAGE

logger = logging.getLogger(__name__)

@contextmanager
@staticmethod
def download(uri: str, session: requests.Session):

    logger.info(f'Downloading "{uri}"...')
    with session.get(uri) as response:
        response.raise_for_status()
        yield response
        

@contextmanager
def download_temp_file(uri: str, session: requests.Session):   

    # Get filename from URL
    filename = Path(urllib.parse.urlsplit(uri).path).name

    with download(uri, session=session) as response:
        # Store file on local disk
        with tempfile.TemporaryDirectory() as directory:
            with Path(directory).joinpath(filename).open('wb') as file:
                file.write(response.content)
                yield file


def remove_emoji(s: str, lang: str = None) -> str:
    """
    Remove emojis, which could break PDF output

    https://carpedm20.github.io/emoji/docs/#replacing-and-removing-emoji
    """

    def replace(s, data_dict):
        nonlocal lang

        try:
            return data_dict[lang]
        # If this language isn't there, default
        except KeyError:
            return data_dict[LANGUAGE]

    # Replace emoji symbols with text representation
    return emoji.replace_emoji(s, replace=replace)


def get_session(**kwargs) -> requests.Session:
    session = requests.Session()

    # Configure backoff strategy
    retry = requests.adapters.Retry(total=3, backoff_factor=1)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter=adapter)
    session.mount('https://', adapter=adapter)

    return session
