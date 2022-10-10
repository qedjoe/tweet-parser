import logging
import urllib.parse
import tempfile
from pathlib import Path
from contextlib import contextmanager

import requests

logger = logging.getLogger(__name__)

session = requests.Session()

@contextmanager
@staticmethod
def download(uri: str):
    logger.info(f'Downloading "{uri}"...')
    with session.get(uri) as response:
        response.raise_for_status()
        yield response
        

@contextmanager
def download_temp_file(uri: str):   

    # Get filename from URL
    filename = Path(urllib.parse.urlsplit(uri).path).name

    with download(uri) as response:
        # Store file on local disk
        with tempfile.TemporaryDirectory() as directory:
            with Path(directory).joinpath(filename).open('wb') as file:
                file.write(response.content)
                yield file
