# Development

Clone the repo, create a virtual environment, and install in editable mode:

```bash
python -m venv ./venv
pip instal -e .
```

## Unit tests

Automated tests are defined in the `./tests` directory. To run the unit tests, run:

```bash
python -m unittest discover --failfast --verbose
```

# Publishing

## Packaging

This project is packaged. See [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/). See `pyproject.toml` for package metadata.

## Automatic publishing

GitHub Actions is configured for this repository. See the `.github` directory.

## Manual publishing

These commands require the `build` and `twine` packages.

To build the package:

```bash
python -m build
```

To upload to the Python package index ([pypi](https://pypi.org)):

```bash
twine upload dist/*
```

