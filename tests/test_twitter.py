import imp
import unittest
from pathlib import Path

import tweets2pdf.twitter

class TwitterTestCase(unittest.TestCase):

    # Assume JSON files are in the current directory
    ROOT_DIR = Path('.')

    @classmethod
    def iter_tweet_files(cls):
        for pattern in {'*.json', '*.js'}:
            yield from cls.ROOT_DIR.glob(pattern)
    
    def test_parse_twitter_archive(self):
        """
        Test the Twitter archive parsing functionality
        """

        # Iterate over JSON files
        for path in self.iter_tweet_files():
            with self.subTest(path=path):
                tweets = tweets2pdf.twitter.read_twitter_json(path)

                for tweet in tweets:
                    tweets2pdf.twitter.simplify_tweet(tweet)

