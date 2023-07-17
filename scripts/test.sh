#!/bin/bash
# basic reference for writing script for travis

VERSION=${1:-6.0}

poetry shell
poetry install --with test

alias ffmpeg='docker jrottenberg/ffmpeg:{version}-scratch'

pytest ./src --cov=./src -s
