
[![CI Tests](https://img.shields.io/github/actions/workflow/status/AaltoPML/VAI-Lab/pythonpackage.yml?branch=main&label=CI%20Test&logo=github)](https://github.com/AaltoPML/VAI-Lab/actions/workflows/documentation.yml) [![Docs Test](https://img.shields.io/github/actions/workflow/status/AaltoPML/VAI-Lab/documentation.yml?branch=main&label=Docs&logo=github)](https://aaltopml.github.io/VAI-Lab/) [![PyPI Version](https://img.shields.io/pypi/v/vai-lab?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/vai-lab/) [![Python Versions](https://img.shields.io/pypi/pyversions/vai-lab?logo=python&logoColor=white)](https://pypi.org/project/vai-lab/) [![Wheel](https://img.shields.io/pypi/wheel/vai-lab)](https://pypi.org/project/vai-lab/) [![License](https://img.shields.io/pypi/l/vai-lab)](https://pypi.org/project/vai-lab/)



# Virtual Artificially Intelligent Laboratories (VAI-Lab)

![VAILBANNER](https://raw.githubusercontent.com/AaltoPML/VAI-Lab/main/imgs/VAIL_banner_image.png)

VAI-Lab is a modular, easy-to-use framework for Virtual Laboraties for science and design, where Artifical Intelligence assists the user in their goals.

> **Warning**
> This project is currently a work in progress and is intended for wider use when a full release is made.
>
> Users are welcome to use the software in its current state, but should expect to heavily alter source code until full testing has been done.
>
> Consult the development and release schedule for the intended timeline for this project.
>
> Any contributions, forks, or pull requests are very welcome. Feel free to get in touch

# How it Works

The VAI-Lab framework uses a modular, plugin-based architecture.

![PLUGINDIAGRAM](https://raw.githubusercontent.com/AaltoPML/VAI-Lab/main/imgs/VAIL_plugin_diagram.png)

Each module represents a process (e.g. Modelling) and each plugin is a specific implementation of that process (e.g. linear regression).

Modules can be chained, looped and modified in real-time to create a highly customisable framework for the user's requirements.

See the [documentation](https://aaltopml.github.io/VAI-Lab/) for more discussion on the project and usage examples.

# Installation

## Requirements

- Python 3.10+
  
## Install from PyPi

Install the latest pip release into a [virtual environment](https://docs.python.org/3/library/venv.html)
```
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip vai-lab 
```
Alternatively, install the latest pip release into a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
```
conda env create --name vai-lab python=3.10 pip && conda activate vai-lab && python3 -m pip install vai-lab
```

## Install from source 

Clone this repository and change directory
```bash,
git clone https://github.com/AaltoPML/VAI-lab.git && cd VAI-lab
```
Install into a [virtual environment](https://docs.python.org/3/library/venv.html)
```bash
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install .
```
Alternatively, , install into a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
```bash
conda create --file environment.yml && conda activate vai-lab-env
```

## Install development dependencies and run tests

In order to run tests using [pytest](https://docs.pytest.org/en/7.3.x/), install the optional development dependencies.

Clone this repository and change directory
```bash,
git clone https://github.com/AaltoPML/VAI-lab.git && cd VAI-lab
```
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

# Documentation

Documentation is available [here](https://aaltopml.github.io/VAI-Lab/). Alternatively, you can build the documentation locally as follows.

Clone this repository and change directory
```bash,
git clone https://github.com/AaltoPML/VAI-lab.git
cd VAI-lab
```
Install the dependencies into a [virtual environment](https://docs.python.org/3/library/venv.html)
```bash
python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install -r sphinx-requirements.txt
```
Alternatively, , install into a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
```bash
conda create --file sphinx-environment.yml && conda activate sphinx-env
```

Build the documentation with
```
sphinx-apidoc --templatedir docs/templates/apidoc -o docs/source src/vai_lab
sphinx-build -M html docs/source docs/build
```
The generated HTML pages are in `docs/build/html`. A good place to start is `docs/build/html/index.html`.



# Feature and Release Schedule :calendar:

- [ ] October/ November 2022: Public repo, API fixing, Testing
- [ ] January 2023: Representative use case release
- [ ] Spring 2023: Initial full release of manual pipeline
- [ ] Fall 2023: Initial release of preliminary AI-Assistance

# How to Contribute

The aim of this framework is to be a community effort that will benefit science, engineering and more.

We are actively seeking contribution in the form of users, testers, developers, and anyone else who would like to contribute.

 - If you have methods which can be added to the framework, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - If you think this framework will be useful to your research, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - If want to get invovled in development, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - Noticed a bug or other issue? [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!


