#!/bin/bash
# basic reference for writing script for travis

version=${1:-6.0}
curl -sSL https://install.python-poetry.org | python3 -

# Add the FFmpeg PPA (Personal Package Archive)
add-apt-repository ppa:jonathonf/ffmpeg-"$version"

# Update the package lists
apt update

# Install FFmpeg with the specified version
apt install ffmpeg="$version"

poetry install --with test

poetry run pytest ./src --cov=./src -s
