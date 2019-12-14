#!/bin/sh
python setup.py build_ext -i
python -c 'import cmatch; Q = cmatch.main()'
python matcher.py
