#!/bin/bash
# basic reference for writing script for travis

FFMPEG_DOCKER_VERSION=${1:-6.0} poetry run pytest ./src --cov=./src -s -m "ffmpeg_version" "$2" --cov-append
