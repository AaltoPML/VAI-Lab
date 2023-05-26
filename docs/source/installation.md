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

