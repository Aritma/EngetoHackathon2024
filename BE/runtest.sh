#!/usr/bin/env bash

python3 -m coverage run --source=. --omit=tests/* -m unittest discover -s tests/
python3 -m coverage report