import unittest
import tempfile
import datetime
from pathlib import Path

import requests

import tweets2pdf.pdf
import tweets2pdf.tweet

class PDFTestCase(unittest.TestCase):
    def setUp(self):
        self.pdf = tweets2pdf.pdf.PDFDocument()

    def tearDown(self):
        with tempfile.TemporaryDirectory() as temp_dir:       
            name = Path(temp_dir).joinpath('test.pdf')
            self.pdf.output(name)

    def test_add_tweet(self):
        tweet_data = dict(
            created_at="Wed Apr 20 18:58:12 +0000 2022",
            id_str= "1516853757119590403",
            full_text="Hello world!",
            extended_entities=dict(),
            entities=dict(
                urls=[
                    dict(
                        url="https://t.co/MEQuGtt2Kh",
                        expanded_url= "https://www.amazon.com/dp/0879232153/ref=nosim?tag=ufojoe-20",
                    ),
                ],
            )
        )
        tweet = tweets2pdf.tweet.Tweet(tweet_data)
        self.pdf.add_tweet(tweet)

    def test_add_image(self):
        uri = 'https://ia800905.us.archive.org/33/items/clevelandart-1921.11-the-fairy-of-the-alp/1921.11_full.jpg'

        with requests.Session() as session:
            self.pdf.add_image(uri, session=session)
