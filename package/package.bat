@echo off


rd /s /q build
python -m poetry run python setup.py build

pause