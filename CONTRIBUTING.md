# Development

Clone the repo, create a virtual environment, and install in editable mode:

```bash
python -m venv ./venv
pip instal -e .
```

# Packaging

See [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

See `pyproject.toml` for package metadata.

## Manual release publishing

These commands require the `build` and `twine` packages.

To build the package:

```bash
python -m build
```

To upload to the Python package index ([pypi](https://pypi.org)):

```bash
twine upload dist/*
```

