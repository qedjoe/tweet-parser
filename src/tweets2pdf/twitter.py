import json
from pathlib import Path
from typing import Iterator
from collections.abc import Mapping, Sequence
import urllib.parse
from http import HTTPStatus
import logging

import dateutil.parser
import emoji

from .settings import ENCODING, LANGUAGE

logger = logging.getLogger(__name__)


def read_twitter_json(path: Path, encoding=None) -> Sequence[Mapping]:
    encoding = encoding or ENCODING

    # Load input file into memory
    with path.open(encoding=encoding) as file:
        data = file.read()

    # Remove everything before the first square bracket
    data = '[' + data.partition('[')[2]

    # Parse JSON
    return [doc['tweet'] for doc in json.loads(data)]


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

def simplify_tweet(tweet: Mapping, username: str = None, language: str = None) -> Mapping:
    """
    Gets data from tweet and returns a simplified data structure

    :returns: Simplified object
    """

    # Language code ISO 639-1
    lang = tweet.get('lang', language or LANGUAGE)

    # Remove undetermined language (any language match) or artificial language
    if lang in {'und', 'art'}:
        lang = None

    # Map Twitter short-URLs to full URLs
    urls = {url['url']: url['expanded_url'] for url in tweet['entities']['urls']}
    images = set()

    # Get media URLs (these also map to short urls) and add these to the short-URL map
    try:
        for media in tweet['extended_entities']['media']:
            urls[media['url']] = media['media_url']
            images.add(media['media_url'])
    except KeyError:
        pass

    # Process message body
    # Remove emoji characters (these don't convert to PDF very well)
    full_text = remove_emoji(tweet['full_text'], lang=lang)

    # Remove crazy characters, which will also break PDF
    # https://docs.python.org/3/howto/unicode.html
    try:
        full_text = full_text.encode('utf-8').decode('unicode-escape')
    except UnicodeDecodeError as exc:
        logger.error(exc)
        logger.warning(full_text)
        pass

    # Convert short urls (t.co) into their original links
    for short_url, expanded_url in urls.items():
        full_text = full_text.replace(short_url, expanded_url)

    return dict(
        created_at=dateutil.parser.parse(tweet['created_at']),
        # Get the set of all hashtags
        hashtags={tag['text'] for tag in tweet['entities']['hashtags']},
        full_text=full_text,
        # Build the original URL of the tweet
        uri=f"https://twitter.com/{username or '_'}/status/{tweet['id_str']}",
        images=images,
    )
