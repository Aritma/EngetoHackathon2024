#!/bin/bash

python3 -m coverage run -m unittest discover -s tests
python3 -m coverage report