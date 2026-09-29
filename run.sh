#!/bin/sh
# Запуск эмулятора: ./run.sh
# Запуск тестов:    ./run.sh test
cd "$(dirname "$0")" || exit 1
if [ "$1" = "test" ]; then
	PYTHONPATH=src python3 -m unittest discover -s tests -v
else
	python3 src/shell.py "$@"
fi