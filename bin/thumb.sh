#!/bin/bash
echo $0
if [[ "$CONDA_DEFAULT_ENV" != "py7" ]]; then
    echo Activating py7...
    eval "$(conda shell.bash hook)"
    conda activate py7
fi
python src/web/thumb.py "$@"
