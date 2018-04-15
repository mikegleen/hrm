LASTMONTH=`python -c "import datetime as dt;print(f'{(dt.date.today() - dt.timedelta(days=dt.date.today().day)).month:02}')"`
echo $LASTMONTH
