#!/bin/bash
# basic reference for writing script for travis


poetry install --with dev

poetry run pre-commit run --all-files
