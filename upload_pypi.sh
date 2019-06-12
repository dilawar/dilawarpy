#!/usr/bin/env bash
set -x
set -e
rm -rf dist
nosetests src
python setup.py sdist
twine check dist/* && twine upload dist/*
