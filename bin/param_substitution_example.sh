#!/bin/zsh
# See: https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
set -e
pushd ~/pyprj/hrm
for fn in modes/data/new_hi_res/*; do
echo fn =     $fn
bn=$(basename -- $fn)
echo    $fn -- ${bn}
echo    $fn -- ${bn%.*}
echo    $fn -- ${bn%%.*}
# sips -s format jpeg -s formatOptions 80  "$fn" --out modes/data/new_hi_res_jpg/${bn%.*}.jpg
done
