#!/usr/bin/env bash
if [[ "$CONDA_DEFAULT_ENV" != "py6" ]]; then
    echo Activating py6...
    . activate py6
fi
python src/web/thumb.py "$@"
