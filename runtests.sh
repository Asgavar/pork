#!/usr/bin/env sh

python -m flake8
python -m mypy -p pork --ignore-missing-imports
python -m pytest -v
