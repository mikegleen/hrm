#!/bin/bash
#
# Produce the monthly Ticket Sales Report for last month.
#
# Parameters:
#   1. The file created by the Store Operations Manager, the "Detailed Ticket
#       Report by Date"
# 
# Output:
#   XLSX file to ~/pyprj/hrm/results/tickets/${LASTYEAR}-${LASTMONTH}
#
# Note the Excel macro to reformat the output is: Ctrl-Shift-A
#    (replaced by pretty2.py)
#
set -e
if [[ "$CONDA_DEFAULT_ENV" != "py6" ]]; then
    echo Activating py6...
    . activate py6
fi
pushd ~/pyprj/hrm
mkdir -p temp
TEMP=temp/clean_tickets.csv
python src/tickets/clean.py "$1" ${TEMP}
# LASTYEAR is the year of last month. It will only be the actual last year if this month is January.
LASTYEAR=`python -c "import datetime as dt;print((dt.date.today() - dt.timedelta(days=dt.date.today().day)).year)"`
LASTMONTH=`python -c "import datetime as dt;print(f'{(dt.date.today() - dt.timedelta(days=dt.date.today().day)).month:02}')"`
eval OUTDIR="~/pyprj/hrm/results/tickets/${LASTYEAR}-${LASTMONTH}"
mkdir -p ${OUTDIR}
python src/tickets/daily.py ${TEMP} -m ${LASTMONTH} -o ${OUTDIR}
python src/tickets/weekly.py ${TEMP} -m ${LASTMONTH} -o ${OUTDIR}
python src/tickets/pretty2.py ${OUTDIR} ${OUTDIR}/tickets_${LASTYEAR}-${LASTMONTH}_merged.xlsx
# rm $TEMP
