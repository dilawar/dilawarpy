#!/usr/bin/env bash
set -x
set -e
rm -rf dist
nosetests3 dilawar
python3 setup.py sdist
python3 -m twine check dist/* && twine upload dist/*
