# -*- coding: utf-8 -*-
"""
Produce a report of the daily revenue.
Input is the file produced by clean.py.
"""
import argparse
import datetime as dt
import os.path
import pandas as pd
import sys

OUTDIR = '/Users/mlg/pyprj/hrm/results/tickets'


def getargs():
    parser = argparse.ArgumentParser(
        description='''
        Produce a report of the daily revenue.
        Input is the file produced by clean.py.
        ''')
    parser.add_argument('infile', help='''
         The CSV file that has been cleaned by tickets.clean.py''')
    parser.add_argument('-o', '--outdir', default=OUTDIR,
                        help='''Directory to contain the
        output report file. If omitted, the default is the directory
        "~/pyrpj/hrm/results/analytics/tickets".
        ''')
    parser.add_argument('-m', '--month', type=int,
                        choices=list(range(1, 13)), help='''
    If specified, limit reporting to the given month in the current year.
    If the month specified is greater than the current month, the year is
    last year. This is only used in January when reporting the December data.
    ''')
    args = parser.parse_args()
    if args.month:
        today = dt.date.today()
        args.year = today.year
        if args.month > today.month:
            args.year -= 1
    return args


def main(args):
    incsvfile = args.infile
    basename = 'tickets_'
    if _args.month:
        basename += f'{args.year:04d}-{args.month:-02d}'
    basename += '_daily.xlsx'
    outreport = os.path.join(args.outdir, basename)
    df = pd.read_csv(incsvfile,
                     usecols=(0, 1, 2, 4),
                     names='date quantity type totprice'.split(),
                     index_col=False)
    df.date = pd.to_datetime(df.date, format='%d/%m/%Y')
    if args.month:
        m = df.date.dt.month
        y = df.date.dt.year
        df = df[(m == args.month) & (y == args.year)]
        assert len(df.date) > 0, f'No data in {args.year}-{args.month:02}.'
    g = df.groupby(['date', 'type'])
    gg = g.sum().unstack().fillna('')
    gg['datetot'] = df.groupby('date').sum()['totprice']
    print(f"Writing to: {outreport}.")
    gg.to_excel(outreport)


if __name__ == '__main__':
    assert sys.version_info >= (3, 8)
    _args = getargs()
    main(_args)
    print('End daily.')
