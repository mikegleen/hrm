#!/bin/bash
echo $0
if [[ "$CONDA_DEFAULT_ENV" != "py6" ]]; then
    echo Activating py6...
    eval "$(conda shell.bash hook)"
    conda activate py6
fi
python src/web/thumb.py "$@"
