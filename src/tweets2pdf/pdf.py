from http import HTTPStatus
import logging
from pathlib import Path

import requests
import fpdf

import tweets2pdf.utils
from .settings import FONT_FAMILY, FONT_SIZE, FONT, IMAGE_WIDTH, UNIT
from .tweet import Tweet

logger = logging.getLogger(__name__)


class PDFDocument:
    """
    Create a PDF document using PyFPDF
    https://pyfpdf.readthedocs.io/en/latest/
    """

    def __init__(self, font: Path = None, font_family: str = None, font_size: float = None, unit:str =None, style: str=None, line_height:float = None, **kwargs):
        self.unit = unit or UNIT
        self.pdf = fpdf.FPDF(unit=self.unit, **kwargs)
        self.font = Path(font or FONT)
        self.font_family = font_family or FONT_FAMILY
        self.font_size = font_size or FONT_SIZE
        self.style = style or ''
        self.height = line_height or self.font_size * 0.6

        # Use a Unicode font so we can use full UTF-8 character set
        # https://pyfpdf.readthedocs.io/en/latest/Unicode/index.html
        self.pdf.add_font(family=self.font_family, style=self.style, fname=self.font, uni=True)
        self.pdf.set_font(family=self.font_family, style=self.style, size=self.font_size)

        self.pdf.add_page()

    def add_tweet(self, tweet: Tweet, height: float = None, download_images: bool = False, image_width = None, session: requests.Session = None):
        """
        Append the tweet to the PDF document
        """

        image_width = image_width or IMAGE_WIDTH

        # Line height
        height = height or self.font_size * 0.6

        # Timestamp
        self.cell(tweet.created_at.isoformat())
        # Hyperlink to Tweet
        self.cell(tweet.uri, link=tweet.uri)
        # Text body
        self.multi_cell(tweet.full_text)

    
        # Embed the image
        for image_uri in tweet.images:
            if download_images:
                try:
                    self.add_image(image_uri, w=image_width, session=session)
                except requests.HTTPError as exc:
                    logger.error(exc)
                    logger.warning('Skipping image')
            self.cell(image_uri, link=image_uri)

    def add_image(self, image_uri: str, session: requests.Session, w = None, **kwargs):
        # Download image
        with tweets2pdf.utils.download_temp_file(image_uri, session=session) as file:
            try:
                # Insert picture into PDF document
                self.pdf.image(file.name, link=image_uri, w=w or 50, **kwargs)
            
            # Handle errors e.g. image format incompatibilities
            except RuntimeError as exc:
                logger.error(exc)
                logger.warning('Skipping image')

    def output(self, name, *args, **kwargs):
        logger.info('Writing PDF file...')
        self.pdf.output(name=name, *args, **kwargs)
        logger.info('Wrote PDF file "%s"', name)

    def line_break(self, height: int = 10):
        self.pdf.ln(h=height)

    def cell(self, text:str, width=0, height=None, ln: int = 1, **kwargs):
        self.pdf.cell(w=width, h=height or self.height, txt=text, ln=ln, **kwargs)

    def multi_cell(self, txt, width = 0, height = None, border:str = None, align: str = None, **kwargs):
        self.pdf.multi_cell(w=width, h=height or self.height, txt=txt, border=border or 'B', align=align or 'L', **kwargs)
