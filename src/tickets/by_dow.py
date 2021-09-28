import argparse
import calendar
import os
import sys
import pandas as pd

OUTDIR = '/Users/mlg/pyprj/hrm/results/analytics/tickets'


def main(incsvfile, outfile):
    df = pd.read_csv(incsvfile,
                     names='date quantity type totprice'.split(),
                     usecols=(0,1,2,4),
                     index_col=False)
    df.date = pd.to_datetime(df.date, format='%d/%m/%Y')
    if _args.start_date:
        df = df[df.date >= _args.start_date]
    if _args.end_date:
        df = df[df.date <= _args.end_date]
    dow = list(calendar.day_abbr)

    df['dayofweek'] = df.date.dt.dayofweek
    # df['nameofday'] = df.dayofweek.apply(lambda x: dow[x])

    dg = df.groupby('dayofweek',as_index=False)
    ds=dg.sum()
    ds['dayname']=ds.dayofweek.apply(lambda x: dow[x])

    ds.to_excel(outfile)


def getargs():
    parser = argparse.ArgumentParser(
        description='''
        Produce a report of the weekly revenue.
        Input is the file produced by clean.py.
        ''')
    parser.add_argument('infile', help='''
         The CSV file that has been cleaned by tickets/clean.py''')
    parser.add_argument('outfile', help=f'''File to contain the output
    XLSX file.''')
    parser.add_argument('-s', '--start_date', help='''
         Include dates greater than or equal to this date (in format YYYY-MM-DD)
         .''')
    parser.add_argument('-e', '--end_date', help='''
         Include dates less than or equal to this date (in format YYYY-MM-DD).
         ''')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        raise ImportError('requires Python 3.6')
    _args = getargs()
    with open(_args.infile) as inf:
        line = inf.readline()
        if line.startswith(';'):
            print('The input file is the raw CSV file. You must use the'
                  ' cleaned file.')
            sys.exit(-1)
    main(_args.infile,  _args.outfile)
    print('End by_dow.')
