import datetime
import json
from pathlib import Path
from collections.abc import Mapping, Set
import logging
from typing import Iterable

import dateutil.parser

from .settings import ENCODING, LANGUAGE, START_CHARACTER
from .utils import remove_emoji

logger = logging.getLogger(__name__)

class Tweet:

    # Tweet URIs don't care what username you use
    NULL_USERNAME = '_'

    def __init__(self, data: Mapping, language: str = None, username: str = None):
        # This is the raw data format from the Twitter archive file
        self._data = data
        self._language = language or LANGUAGE
        self.username = username or self.NULL_USERNAME
        self._created_at = None

    @staticmethod
    def load(path: Path, encoding=None, start_char: str = None) -> Iterable[Mapping]:
        encoding = encoding or ENCODING
        start_char = start_char or START_CHARACTER

        # Load input file into memory
        # (Ideally we'd stream this, but the unpredictable format prevents this.)
        with path.open(encoding=encoding) as file:
            data = file.read()

        # Remove everything before the first square bracket
        data = data[data.find(start_char):]

        # Parse JSON
        # Each object in the document has a 'tweet' key
        for doc in json.loads(data):
            yield doc['tweet']

    @property
    def language(self) -> str:        

        # Language code ISO 639-1
        lang = self._data.get('lang', self._language)

        # Remove undetermined language (any language match) or artificial language
        if lang in {'und', 'art'}:
            lang = None

        return lang

    @property
    def created_at(self) -> datetime.datetime:
        if self._created_at is None:
            self._created_at = dateutil.parser.parse(self._data['created_at'])
        return self._created_at

    @property
    def urls(self) -> Mapping[str, str]:
        """
        Map Twitter short-URLs to full URLs so they can be replaced in the
        main Tweet body text.
        """
        urls = dict()
        
        try:
            for media in self._data['extended_entities']['media']:
                urls[media['url']] = media['media_url']
        except KeyError:
            pass

        for url in self._data['entities']['urls']:
            urls[url['url']] = url['expanded_url']

        return urls

    @property
    def images(self) -> set:
        images = set()

        # Get media URLs (these also map to short urls) and add these to the short-URL map
        # This media key might not exist
        try:
            for media in self._data['extended_entities']['media']:
                images.add(media['media_url'])
        except KeyError:
            pass

        return images

    @property
    def full_text(self) -> str:
        
        # Process message body
        # Remove emoji characters (these don't convert to PDF very well)
        full_text = remove_emoji(self._data['full_text'], lang=self.language)

        # Remove crazy characters, which will also break PDF
        # https://docs.python.org/3/howto/unicode.html
        try:
            full_text = full_text.encode('utf-8').decode('unicode-escape')
        except UnicodeDecodeError as exc:
            logger.error(exc)
            logger.warning(full_text)
            pass

        # Convert short urls (t.co) into their original links
        for short_url, expanded_url in self.urls.items():
            full_text = full_text.replace(short_url, expanded_url)

        return full_text

    @property
    def _hashtags(self):
        return self._data['entities']['hashtags']

    @property
    def hashtags(self) -> Set[str]:
        return {hashtag['text'].casefold() for hashtag in self._hashtags}

    @property
    def id_str(self) -> str:
        return self._data['id_str']

    @property
    def uri(self) -> str:
        """
        The full web address of this tweet.
        """
        return f"https://twitter.com/{self.username}/status/{self.id_str}"
