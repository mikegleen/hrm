#!/usr/bin/env bash
#
# Produce a Ticket Sales Report for all dates in the input file.
#
# Parameters:
#   1. The file created by the Store Operations Manager, the "Detailed Ticket
#       Report by Date"
#
# Output:
#   XLSX file to ~/pyprj/hrm/results/tickets/full/${TODAY}
#
TICKETENV=py6
set -e
if [[ "$CONDA_DEFAULT_ENV" != "$TICKETENV" ]]; then
    echo Activating ${TICKETENV}
    . activate ${TICKETENV}
fi
pushd ~/pyprj/hrm
mkdir -p temp
TEMP=temp/clean_tickets.csv
python src/tickets/clean.py "$1" ${TEMP}
TODAY=`date +%Y-%m-%d`
eval OUTDIR="~/pyprj/hrm/results/tickets/full/${TODAY}"
mkdir -p ${OUTDIR}
python src/tickets/weekly.py ${TEMP} -o ${OUTDIR}
# rm $TEMP
