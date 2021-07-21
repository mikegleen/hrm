#!/bin/bash
echo $0
if [[ "$CONDA_DEFAULT_ENV" != "py8" ]]; then
    echo Activating py8...
    eval "$(conda shell.bash hook)"
    conda activate py8
fi
python src/web/thumb.py "$@"
