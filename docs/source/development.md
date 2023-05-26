# Development

## Clone repository

To get started with development, clone the VAI-lab repository and change directory
```bash,
git clone https://github.com/AaltoPML/VAI-lab.git && cd VAI-lab
```

## Run tests locally

To run tests locally, first install the optional development dependencies.

Install into a [virtual environment](https://docs.python.org/3/library/venv.html)
```bash
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install ".[dev]"
```

Alternatively, , install into a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
```bash
conda create --file dev-environment.yml && conda activate dev-vai-lab-env
```

Run unit tests with pytest
```bash
pytest .
```

## CI tests

Tests are run automatically for all pull requests using the GitHub Actions workflow specified in the file `.github/workflows/pytest.yml` 


## Build documents locally

To build documentation locally using [Sphinx](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/), first install the dependencies.

Install the dependencies into a [virtual environment](https://docs.python.org/3/library/venv.html)
```bash
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install -r sphinx-requirements.txt
```

Alternatively, install into a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
```bash
conda create --file sphinx-environment.yml && conda activate sphinx-env
```

Build the documentation with
```
sphinx-build -M html docs/source docs/build
```
The HTML pages are genereated in `docs/build/html`. A good place to start is `docs/build/html/index.html`.

## CI document building

Documentation is built and published to [GitHub pages](https://pypi.org/project/vai-lab/) automatically for all pull requests using the GitHub Actions workflow specified in the file `.github/workflows/sphinx.yml`.

