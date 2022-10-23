import unittest
import tempfile
from pathlib import Path

import tweets2pdf.twitter
import tweets2pdf.pdf


class TwitterTestCase(unittest.TestCase):

    @classmethod
    def iter_tweet_files(cls):
        # Find JSON files in various directories
        for pattern in {'*.json', '*.js'}:
            # Assume JSON files are in the current directory
            yield from Path('.').glob(pattern)
            # Search current working directory
            yield from Path.cwd().glob(pattern)

    def iter_tweet_collections(self):                
        # Iterate over JSON files
        for path in self.iter_tweet_files():
            with self.subTest(path=str(path)):
                yield tweets2pdf.twitter.read_twitter_json(path)

    def test_build_pdf(self):
        # Create a PDF document for each input Twitter archive
        for tweets in self.iter_tweet_collections():
            pdf = tweets2pdf.pdf.PDFDocument()

            # Add tweets to the document
            for tweet in tweets:
                tweet = tweets2pdf.twitter.simplify_tweet(tweet)
                pdf.add_tweet(tweet)
            
            # Write an output file (this takes time)
            with tempfile.TemporaryDirectory() as tmpdir:
                name = str(Path(tmpdir).joinpath('output.pdf'))
                pdf.output(name)
