# Fake data generator

## Supported providers

https://faker.readthedocs.io/en/master/providers.html

## Setup Development Environment

### Install Python Virtual Environment

```python -m venv .venv```

(use `python3` if you are on macOS)

### Install Dependencies

Open `vscode` from the root folder. `vscode` will detect `.venv` once
we open a python source file. 

Open a new terminal, and install dependencies.

```pip install -r requirements-dev.txt```

(use `pip3` if you are on macOS)

## Test run

To generate fake data in pandas dataframe with random seed.
```python main_df.py```

or

To generate fake data for statement (5 times).
```python main_template.py```