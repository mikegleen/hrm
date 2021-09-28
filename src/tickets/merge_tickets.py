# -*- coding: utf-8 -*-
"""
    Clean and merge ticket report files.

    Clean the Ticket Report file. (Copied from clean.py)
    1. Delete the first 4 lines of title, comments, etc.
    2. Convert the input latin-1 (iso-8859-1) input to utf-8
    3. Delete lines starting with ' ' which are summary lines.


"""
import codecs
import datetime
import os.path
import re
import sys

FILENAMEPAT = r'tickets_\d{4}-\d{2}(_\d{4}-\d{2})*.csv'
SKIPLINES = 4


def main(infile, outfile):
    global alldates  # contains dates found in previous files
    print(f'Processing {infile.name}.')
    newdates = set()
    if SKIPLINES:
        line = next(infile)
        if line[0] != ';':
            print(f'Input file {infile.name} is not a raw CSV file.')
        for i in range(SKIPLINES - 1):
            next(infile)
    nlines = 0
    for line in infile:
        if line[0] != ' ':
            d = datetime.datetime.strptime(line[:10], '%d/%m/%Y').date()
            if d in alldates:
                print(f'Duplicate date {d} in {infile.name}')
                return
            newdates.add(d)
            outfile.write(line)
            nlines += 1
    alldates |= newdates
    print(f'   {nlines} written.')


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) <= 2:
        print('Two parameters needed, the directory containing original ticket'
              ' reports and the output cleaned file.')
        sys.exit(1)
    alldates = set()
    indir = sys.argv[1]
    outf = sys.argv[2]
    if not os.path.isdir(indir):
        print('First parameter must be a directory containing the original'
              ' ticket reports.')
        sys.exit(2)
    outcsv = open(outf, 'w')
    for inf in sorted(os.listdir(indir)):
        m = re.match(FILENAMEPAT, inf)
        if not m:
            print(f'Filename ignored: {inf}.')
            continue
        inpath = os.path.join(indir, inf)
        with codecs.open(inpath, 'r', 'latin_1') as incsv:
            main(incsv, outcsv)
    print('End merge_tickets.')
