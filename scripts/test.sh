#!/bin/bash
# basic reference for writing script for travis

curl -sSL https://install.python-poetry.org | python3 -

poetry install --with test


FFMPEG_DOCKER_VERSION=${1:-6.0} poetry run pytest ./src --cov=./src -s -m "ffmpeg_version" "$2" --cov-append
