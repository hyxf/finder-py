#!/usr/bin/env bash

./clean.sh

pip uninstall finder

python setup.py build
python setup.py install

echo '=====install====='