# -*- coding: utf-8 -*-
"""
    Consolidate the weekly reports from Google Analytics and produce a CSV file
    with one row for each week.

    Assume a fixed format of the weekly analytics file.
    Skip the first 13 rows.
    The first parameter on row 14 is the week-ending date (on a Thursday).
    The 2nd parameter on row 15 is the week's total hits.
"""
import datetime
import os.path
import sys


def main(audiencedir, outcsvf):
    outfile = open(outcsvf, 'w')
    infiles = os.listdir(audiencedir)
    for filename in infiles:
        if not filename.endswith('.csv'):
            continue
        filepath = os.path.join(audiencedir, filename)
        with open(filepath) as csvf:
            for i in range(13):
                csvf.readline()
            datestr, _ = csvf.readline().split(',')
            weekending = datetime.datetime.strptime(datestr,'%d/%m/%Y').date()
            weekending = weekending.isoformat()
            row = csvf.readline().strip()[1:]  # remove leading ','
            if row[0] == '"':
                row = row[1:-1]  # strip leading and trailing quote
            count = row.replace(',', '')  # remove embedded comma
            # print(row)
            # noinspection PyTypeChecker
            print(f'{weekending},{count}', file=outfile)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Two parameters needed, the input directory. and output file.')


