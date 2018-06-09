#!/usr/bin/env sh

python -m flake8
python -m mypy -p pork
python -m pytest -v
