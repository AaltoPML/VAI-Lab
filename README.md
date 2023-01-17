
[![CI Tests](https://img.shields.io/github/actions/workflow/status/AaltoPML/VAI-Lab/pythonpackage.yml?branch=main&label=CI%20Test&logo=github)](https://github.com/AaltoPML/VAI-Lab/actions/workflows/documentation.yml)[![Docs Test](https://img.shields.io/github/actions/workflow/status/AaltoPML/VAI-Lab/documentation.yml?branch=main&label=Docs&logo=github)](https://github.com/AaltoPML/VAI-Lab/actions/workflows/documentation.yml)
[![PyPI Version](https://img.shields.io/pypi/v/vai-lab?color=blue)](https://pypi.org/project/vai-lab/) [![Python Versions](https://img.shields.io/pypi/pyversions/vai-lab?color=blue)](https://pypi.org/project/vai-lab/) [![Wheel](https://img.shields.io/pypi/wheel/vai-lab)](https://pypi.org/project/vai-lab/) [![License](https://img.shields.io/pypi/l/vai-lab)](https://pypi.org/project/vai-lab/)



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

# How to Contribute

The aim of this framework is to be a community effort that will benefit science, engineering and more.

We are actively seeking contribution in the form of users, testers, developers, and anyone else who would like to contribute.

 - If you have methods which can be added to the framework, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - If you think this framework will be useful to your research, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - If want to get invovled in development, [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!
 - Noticed a bug or other issue? [get in touch](https://github.com/AaltoPML/VAI-Lab#get-in-touch)!

# How it Works

The VAI-Lab framework uses a modular, plugin-based architecture.

![PLUGINDIAGRAM](https://raw.githubusercontent.com/AaltoPML/VAI-Lab/main/imgs/VAIL_plugin_diagram.png)

Each module represents a process (e.g. Modelling) and each plugin is a specific implementation of that process (e.g. linear regression).

Modules can be chained, looped and modified in real-time to create a highly customisable framework for the user's requirements.

# Installation

## Installing from package

To install the latest pip release:

```
pip install vai-lab
```

## Installing from source 

Clone this repository via HTTPS:
```bash
git clone https://github.com/AaltoPML/VAI-lab.git
```
OR SSH:
```bash
git clone git@github.com:AaltoPML/VAI-lab.git
```
Change directory
```bash
cd VAI-lab
```
Create a virtual environment and activate it using venv
```bash
python3 -m venv venv && source venv/bin/activate
```
or, alternatively, using conda environment
```bash
conda create --name vai_lab python=3.8 && conda activate vai_lab
```
Upgrade pip
```bash
python3 -m pip install -U pip
```
Install the package
```bash
python3 -m pip install .
```

# Running Unit Tests

Unit tests are run with pytest with
```bash
pytest
```

# Feature and Release Schedule :calendar:

- [ ] October/ November 2022: Public repo, API fixing, Testing
- [ ] January 2023: Representative use case release
- [ ] Spring 2023: Initial full release of manual pipeline
- [ ] Fall 2023: Initial release of preliminary AI-Assistance

# Get in Touch
If you would like contribute, test, give feedback, or ask questions about this framework, we'd like to hear from you!
Email us at:
- Chris McGreavy, chris.mcgreavy [at] aalto.fi
- Carlos Sevilla-Salcedo, carlos.sevillasalcedo [at] aalto.fi
