# -*- coding: utf-8 -*-
"""
Produce a report of the weekly revenue by day of the week.
Input is the file produced by clean.py.
"""

import argparse
from openpyxl import Workbook, load_workbook
import datetime as dt
import os.path
import pandas as pd
import sys

from config import ADMISSION_TYPES


OUTDIR = '/Users/mlg/pyprj/hrm/results/analytics/tickets'

# df[df['A'].isin([3, 6])]

# Exclude those weeks when an exhibition opens because it opens on Saturday
# while the special exhibition is closed on the preceding Thursday & Friday.
# The dates shown are the Monday of a week to skip.
#
# SKIPWEEKS is a list of strings each in the format: yyyy-mm-dd
# SKIPLIST is used to build SKIPWEEKS and contains sub-lists where the first
# entry is the year and the 2nd through nth entries are 2-lists of the month
# and day of the affected weeks.

SKIPLIST = [[2017, [1, 9], [3, 27], [6, 12], [11, 27]],
             [2018, [2, 17], [5, 21], [8,20], [11,19]],
             [2019, [2, 18], [5, 20], [8, 26], [11,17]]
            ]
SKIPWEEKS = []

for yl in SKIPLIST:
    SKIPWEEKS += [f'{yl[0]}-{m[0]:02d}-{m[1]:02d}' for m in yl[1:]]


def one_report(df, suffix):
    basename = 'tickets_'
    if _args.month:
        basename += f'{_args.year:04d}-{_args.month:-02d}_'
    basename += 'weekly_' + suffix + '.xlsx'
    outreport = os.path.join(_args.outdir, basename)
    g = df.groupby(['date', 'dayofweek'])
    gg = g.sum().unstack().fillna('')
    gg['weektot'] = df.groupby('date').sum()['totprice']
    print(f"Writing to: {outreport}.")
    gg.to_excel(outreport)


def main():
    incsvfile = _args.infile
    df = pd.read_csv(incsvfile,
                     names='date quantity type totprice'.split(),
                     usecols=(0, 1, 2, 4),
                     index_col=False)
    dfdate = pd.to_datetime(df.date, format='%d/%m/%Y')
    if _args.month:
        m = dfdate.dt.month
        y = dfdate.dt.year
        df = df[(m == _args.month) & (y == _args.year)]
    #
    df['dayofweek'] = dfdate.dt.dayofweek
    one_report(df, 'full')
    df2 = df[df.type.isin(ADMISSION_TYPES)]
    one_report(df2, 'admission')
    df3 = df[~df.type.isin(ADMISSION_TYPES)]
    one_report(df3, 'other')


def getargs():
    parser = argparse.ArgumentParser(
        description='''
        Produce a report of the weekly revenue.
        Input is the file produced by clean.py.
        ''')
    parser.add_argument('infile', help='''
         The XLSX file that has been cleaned by tickets/clean.py''')
    parser.add_argument('-o', '--outdir', help='''Directory to contain the
        output report file. If omitted, the default is the directory
        "results" in the same directory that the input file resides.
        ''')
    args = parser.parse_args()
    if not args.outdir:
        args.outdir = OUTDIR
    return args


if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        raise ImportError('requires Python 3.6')
    _args = getargs()
    _basename = os.path.split(_args.infile)[1]
    _basename = os.path.splitext(_basename)[0]
    main()
    print('End week_graph.')
