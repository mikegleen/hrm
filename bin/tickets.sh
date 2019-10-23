#!/bin/bash
#
# Produce the monthly Ticket Sales Report for last month or for a specified
# month.
#
# Parameters:
#   1. The file created by the Store Operations Manager, the "Detailed Ticket
#       Report by Date"
#   2. Optional 4-digit year
#   3. Optional 2-digit month (required if parameter 2 is set)
# 
# Output:
#   XLSX file to ~/pyprj/hrm/results/tickets/${LASTYEAR}-${LASTMONTH}
#
TICKETENV=py7
TEMP=temp/clean_tickets.csv
set -e
if [[ "$CONDA_DEFAULT_ENV" != "$TICKETENV" ]]; then
    echo Activating ${TICKETENV}
    eval "$(conda shell.bash hook)"
    conda activate ${TICKETENV}
fi
pushd ~/pyprj/hrm
mkdir -p temp
python src/tickets/clean.py "$1" ${TEMP}
if [ $# -eq 3 ]
then
    LASTYEAR=$2
    LASTMONTH=$3
else
    # LASTYEAR is the year of last month. It will only be the actual last year if this month is January.
    LASTYEAR=`python -c "import datetime as dt;print((dt.date.today() - dt.timedelta(days=dt.date.today().day)).year)"`
    LASTMONTH=`python -c "import datetime as dt;print(f'{(dt.date.today() - dt.timedelta(days=dt.date.today().day)).month:02}')"`
fi
eval OUTDIR="~/pyprj/hrm/results/tickets/${LASTYEAR}-${LASTMONTH}"
mkdir -p ${OUTDIR}
python src/tickets/daily.py ${TEMP} -m ${LASTMONTH} -o ${OUTDIR}
python src/tickets/weekly.py ${TEMP} -m ${LASTMONTH} -o ${OUTDIR}
python src/tickets/pretty2.py ${OUTDIR} ${OUTDIR}/tickets_${LASTYEAR}-${LASTMONTH}_merged.xlsx 
# rm $TEMP
