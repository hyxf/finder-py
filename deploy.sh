#!/usr/bin/env bash

./clean.sh

python setup.py sdist
python setup.py bdist_wheel

twine upload dist/*

echo '=====upload====='