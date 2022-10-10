import tempfile
import logging
from pathlib import Path
from collections.abc import Mapping
from http import HTTPStatus
import urllib.parse

import requests
import fpdf

import tweets2pdf.utils

logger = logging.getLogger(__name__)

session = requests.Session()

class PDFDocument:
    """
    Create a PDF document using PyFPDF
    https://pyfpdf.readthedocs.io/en/latest/
    """

    def __init__(self, font: Path, font_family: str, font_size: float = None, unit:str =None, style: str=None, **kwargs):
        self.pdf = fpdf.FPDF(**kwargs)
        self.font_size = font_size
        self.style = style or ''

        # Use a Unicode font so we can use full UTF-8 character set
        # https://pyfpdf.readthedocs.io/en/latest/Unicode/index.html
        self.pdf.add_font(font_family, style=self.style, fname=font, uni=True)
        self.pdf.set_font(family=font_family, style=self.style, size=self.font_size)

        self.pdf.add_page()

    def add_tweet(self, tweet: Mapping, height: float = None, download_images: bool = False, image_width = None):
        """
        Append the tweet to the PDF document
        """

        # Line height
        height = height or self.font_size * 0.6

        # Timestamp
        self.pdf.cell(w=0, h=height, txt=tweet['created_at'].isoformat(), ln=1)
        # Hyperlink to Tweet
        self.pdf.cell(w=0, h=height, txt=tweet['uri'], link=tweet['uri'], ln=1)
        # Text body
        self.pdf.multi_cell(w=0, h=height, txt=tweet['full_text'], border='B', align='L')

        if download_images:
            for image_uri in tweet['images']:
                self.add_image(image_uri, w=image_width)

    def add_image(self, image_uri: str, w = None, **kwargs):
        # Download image
        with tweets2pdf.utils.download_temp_file(image_uri) as file:
            try:
                # Insert picture into PDF document
                self.pdf.image(file.name, link=image_uri, w=w or 50, **kwargs)
            
            # Handle errors e.g. image format incompatibilities
            except RuntimeError as exc:
                logger.error(exc)
                logger.warning('Skipping image')
                # Put some text in the PDF document as a placeholder
                self.cell(image_uri, link=image_uri)

    def output(self, name, *args, **kwargs):
        logger.info('Writing PDF file...')
        self.pdf.output(name=name, *args, **kwargs)
        logger.info('Wrote PDF file "%s"', name)

    def line_break(self, height: int = 10):
        self.pdf.ln(h=height)

    def cell(self, text:str, width=0, height=None, ln: int = 1, **kwargs):
        # Line height
        height = height or self.font_size * 0.6
        self.pdf.cell(w=width, h=height, txt=text, ln=ln, **kwargs)
