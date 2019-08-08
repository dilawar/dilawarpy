#!/usr/bin/env bash
set -x
set -e
rm -rf dist
nosetests dilawar || echo "Failed test"
python setup.py sdist
twine check dist/* && twine upload dist/*
