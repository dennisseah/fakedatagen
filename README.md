# Fake data generator

## Supported providers

https://faker.readthedocs.io/en/master/providers.html

## Dependencies

- Install pdm (instruction at https://pdm.fming.dev/)

## Setup Development Environment

1. edit `.pdm.toml` to reference your preferred _Python_ interpreter.
1. edit `python.autoComplete.extraPaths` and `python.analysis.extraPaths` in `.vscode/settings.json` to have to correct _Python_ version (currently, it is `3.8`)
1. ```pdm install```

## Test run

To generate fake data in pandas `dataframe` with a random seed.
```sh
export PYTHONPATH=src
python samples/main_df.py
```

or

To generate fake data for statement (5 times).
```sh
python samples/main_json.py
```

or

To generate fake data for statement (5 times).
```sh
python samples/main_strtemplate.py
```

## Test unit tests

```sh
pytest --cov=fake_data_builder --cov-report term-missing tests/
```

## Package wheel

```sh
python3 -m pip install --upgrade build
python -m build
```