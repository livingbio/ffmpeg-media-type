#!/bin/bash
# basic reference for writing script for travis

curl -sSL https://install.python-poetry.org | python3 -

VERSION=${1:-6.0}

poetry shell
poetry install --with test,dev
pre-commit run --all-files

alias ffmpeg='docker jrottenberg/ffmpeg:{version}-scratch'

pytest ./src --cov=./src -s
