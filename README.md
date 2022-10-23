# Tweet archive parser

This is a simple tool to parse Twitter archived JSON files and convert to PDF document file format.    

# Acknowledgements

* [Isaac Koi](https://twitter.com/isaackoi/)
* Forked from [vrruiz/tweet-js](https://github.com/vrruiz/tweet-js)
* [qedjoe](https://twitter.com/qedjoe/)
* [DejaVu Fonts](https://dejavu-fonts.github.io/)

# Installation

Install [Python](https://www.python.org/).

Install this package in your current environment using the command below:

```bash
pip install tweets2pdf
```

## Upgrade

To update to the latest version of this software:

```bash
pip install --upgrade tweets2pdf
```

# Usage

## Download your Twitter archive

See: Twitter Help Centre [How to download your Twitter archive](https://help.twitter.com/en/managing-your-account/how-to-download-your-twitter-archive). Once you have downloaded your archive, look for the `tweets.js` JSON file which contains all your tweets. This code will process that file.

## Run the script

The basic usage is:

```bash
tweets2pdf -f tweets.js --images -p output.pdf
```

The `--images` option enables the downloading of pictures from Twitter, which will make the process *much slower*.

For more details:
```bash
tweets2pdf --help
```

# Development

## Contributing

Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for information about participating in this project.

Please submit bug reports using [GitHub Issues](https://github.com/qedjoe/tweet-parser/issues).

## Deployment status

[![Upload Python Package](https://github.com/qedjoe/tweet-parser/actions/workflows/python-publish.yml/badge.svg)](https://github.com/qedjoe/tweet-parser/actions/workflows/python-publish.yml)
