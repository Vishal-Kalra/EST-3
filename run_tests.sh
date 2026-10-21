#!/usr/bin/env bash
# One command setup + run (macOS / Linux).
#   ./run_tests.sh              run everyone's tests
#   ./run_tests.sh vishal       run only tests/vishal
#   ./run_tests.sh vishal -k S2 extra pytest options go after the name
set -e
cd "$(dirname "$0")"                       # always run from the project folder

if [ ! -d ".venv" ]; then                  # first run: create the virtual environment
  echo "Creating .venv ..."
  python3 -m venv .venv
fi
source .venv/bin/activate                  # use the project's own Python
pip install -q -r requirements.txt         # installs/updates selenium, pytest, pytest-html

if [ -n "$1" ] && [ -d "tests/$1" ]; then  # first argument = your folder name
  target="tests/$1"; shift
else
  target="tests"
fi

pytest "$target" --html=report.html --self-contained-html "$@"
echo ""
echo "Screenshots: screenshots/    HTML report: report.html"
