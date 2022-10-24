#!/usr/bin/env python3

import argparse
import logging
import datetime
import itertools
from typing import Optional

from pathlib import Path

import dateutil.parser
import pytz
import requests

from .tweet import Tweet
from .pdf import PDFDocument
from .settings import ENCODING, LANGUAGE, FONT_FAMILY, FONT_SIZE, FONT, IMAGE_WIDTH
import tweets2pdf.utils

DESCRIPTION = """
Parse Twitter archived JSON files and convert to PDF files
"""


logger = logging.getLogger(__name__)


def utc_timestamp(timestamp: str) -> datetime.datetime:
    """
    Parse user-inputted timestamp
    """
    # Parse timestamp
    t = dateutil.parser.parse(timestamp)
    # Convert to UTC
    return pytz.UTC.localize(t)


def get_args():
    """
    Command-line arguments
    """

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    # Twitter archive options
    parser.add_argument("-f", "--file", type=Path, dest="filename", help="Path to Twitter JSON archive", required=True)
    parser.add_argument('--encoding', default=ENCODING, help='Input file character set')
    parser.add_argument("-a", "--hashtags", help="Filter by hashtags (comma-separated list)", default=str())
    parser.add_argument("-s", "--date_start", dest="date_start", type=utc_timestamp)
    parser.add_argument("-e", "--date_end", dest="date_end", type=utc_timestamp)
    parser.add_argument('--start', type=int, help="Start at this tweet number")
    parser.add_argument('--stop', type=int, help="Stop after this many tweets")

    # PDF output options
    parser.add_argument("-p", "--pdf", type=Path, help='Output PDF file path', required=True)
    parser.add_argument('-i', '--images', help='Download images and put in the PDF document (SLOW)', action='store_true')
    parser.add_argument('-w', '--imgwidth', help="Image width", default=IMAGE_WIDTH)
    
    # Font options
    parser.add_argument('--font', help='Unicode font TTF file', type=Path, default=FONT)
    parser.add_argument('--font_family', default=FONT_FAMILY)
    parser.add_argument('--font_size', type=float, default=FONT_SIZE)
    parser.add_argument('--loglevel', default='INFO', help="Verbosity level: DEBUG, INFO, WARNING, ERROR")
    parser.add_argument('--language', default=LANGUAGE, help='Language ISO 639-1 code')

    return parser.parse_args()


def main():
    options = get_args()
    logging.basicConfig(level=options.loglevel)

    # Get the selected hashtags
    hashtag_filter = {s.strip() for s in options.hashtags.casefold().split(',')}

    pdf = PDFDocument(font=options.font, font_family=options.font_family, font_size=options.font_size)

    # Create a HTTP session if we want to download images
    session: Optional[requests.Session] = None
    if options.images:
        session = tweets2pdf.utils.get_session()

    # Iterate over input tweets
    tweet_count = 0
    for tweet_data in itertools.islice(Tweet.load(options.filename, encoding=options.encoding), options.start, options.stop):
        tweet_count += 1

        # Show progress
        if tweet_count % 1000 == 0:
            logger.info(f"Processing tweet {tweet_count}")

        # Decode tweet in a simple structure
        tweet = Tweet(tweet_data)

        # Time filter
        try:
            if tweet.created_at < options.date_start:
                continue
        except TypeError:
            pass

        try:
            if tweet.created_at >= options.date_end:
                continue
        except TypeError:
            pass

        # Filter by hashtag
        if not tweet.hashtags.union(hashtag_filter):
            continue

        pdf.add_tweet(tweet, download_images=options.images, image_width=options.imgwidth, session=session)

    pdf.output(options.pdf)

    if session is not None:
        session.close()


if __name__ == '__main__':
    main()
