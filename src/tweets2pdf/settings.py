from pathlib import Path

# Input file character set
ENCODING = 'utf-8'
# Where does the JSON data start in the input file?
# Sometimes there is prefixed random data by Twitter
START_CHARACTER = '['

# Default language code
# https://en.wikipedia.org/wiki/ISO_639-1
LANGUAGE = 'en'

FONT_FAMILY = 'DejaVu Sans'
FONT_SIZE = 11
FONT = Path('./font/DejaVuSans.ttf')
UNIT = 'mm'
IMAGE_WIDTH = 150
