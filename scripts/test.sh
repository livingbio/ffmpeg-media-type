#!/bin/bash
# basic reference for writing script for travis

VERSION=${1:-6.0}
curl -sSL https://install.python-poetry.org | python3 -

poetry install --with test

alias ffmpeg='docker jrottenberg/ffmpeg:{version}-scratch'

poetry run pytest ./src --cov=./src -s