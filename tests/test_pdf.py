import unittest
import tempfile
import datetime
from pathlib import Path

import requests

import tweets2pdf.pdf

class PDFTestCase(unittest.TestCase):
    def setUp(self):
        self.pdf = tweets2pdf.pdf.PDFDocument()

    def tearDown(self):
        with tempfile.TemporaryDirectory() as temp_dir:       
            name = Path(temp_dir).joinpath('test.pdf')
            self.pdf.output(name)

    def test_add_tweet(self):
        tweet = dict(
            created_at=datetime.datetime.min,
            uri=f"https://twitter.com/_/status/0",
            full_text="Hello world!",
        )
        self.pdf.add_tweet(tweet)

    def test_add_image(self):
        uri = 'https://ia800905.us.archive.org/33/items/clevelandart-1921.11-the-fairy-of-the-alp/1921.11_full.jpg'

        with requests.Session() as session:
            self.pdf.add_image(uri, session=session)
