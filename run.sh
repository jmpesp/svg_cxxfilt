#!/bin/bash
# run from anywhere, assuming there's a venv at `.venv`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source ${DIR}/.venv/bin/activate
"${DIR}/do.py" "${@}"
