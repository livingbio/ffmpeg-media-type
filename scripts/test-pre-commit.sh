#!/bin/bash
# basic reference for writing script for travis

curl -sSL https://install.python-poetry.org | python3 -

poetry install --with dev

pre-commit run --all-files
