# -*- coding: utf-8 -*-
"""
Convert the dates in the Heath Robinson cartoon transcriptions to ISO 8601
format. This code depends upon knowing what the input file's Date field
contains. If the input file is modified, run the program and for any records
where the ISODate field is "N/A", update the strp_formats tuple as appropriate.

If the year in the date is later than 1999, subtract 100 from the year.

Input: the CSV file produced by read_html.py.
       The file name must end with '.csv'
Output: an XLSX formatted spreadsheet.
Command line arg: the name of the file to process. The input file must be
<name>.csv in the results/csv directory and the output file will be <name>.xlsx
in the results/xlsx directory.

"""

import csv
from datetime import datetime as dt
import os.path
import sys
import xlsxwriter

ISODATE = 'ISODate'
HRMDIR = os.path.join('/', 'Users', 'mlg', 'pyprj', 'hrm')
CSVDIR = os.path.join(HRMDIR, 'results', 'csv')
CSVPATH_TEMPLATE = os.path.join(CSVDIR, '{}.csv')
XLSXDIR = os.path.join(HRMDIR, 'results', 'xlsx')
XLSXPATH_TEMPLATE = os.path.join(XLSXDIR, '{}.xlsx')

# Define the date formats that we know will be in the data.
#
strp_formats = ('%d %b %y',  # 1 Jan 18
                '%d %b %Y',  # 1 Jan 1918
                '%d.%m.%y',  # 1.1.18
                '%d.%m.%Y',  # 1.1.1918
                '%d/%m/%y',  # 1/1/18
                '%d%b %y',   # 1Jan 18
                '%b %y',     # Jan 18
                '%b %Y'      # Jan 1918
                )


def fixdate(rawdate):
    rtn = 'N/A'
    for fmt in strp_formats:
        try:
            # print(rawdate, fmt)
            fixed = dt.strptime(rawdate, fmt)
            if fixed.year > 1999:
                fixed = dt(fixed.year - 100, fixed.month, fixed.day)
            # rtn = fixed.isoformat()[:10]
            rtn = fixed  # .isoformat()[:10]
            break
        except ValueError:
            pass
    return rtn


def main():
    # Get the original heading from the CSV file and add the column for the ISO
    # format date that we will append.
    csvfile = open(csvpath)
    firstline = csvfile.readline()
    csvfile.close()
    fieldnames = firstline.strip().split('|')
    fieldnames += ['ISODate']

    # Open the workbook and put the heading line to the worksheet
    workbook = xlsxwriter.Workbook(xlsxpath)
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0, 0, 86.66)
    worksheet.set_column(1, 2, 14.04)
    worksheet.set_column(3, 5, 12.05)

    wformat = workbook.add_format()
    wformat.set_text_wrap()
    wformat.set_align("vjustify")
    dformat = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    colnum = 0
    for name in fieldnames:
        worksheet.write_string(0, colnum, name, wformat)
        colnum += 1
    # print(CSVPATH)

    csvfile = open(csvpath, 'r')
    reader = csv.DictReader(csvfile, delimiter='|',)
    rownum = 1
    for row in reader:
            row[ISODATE] = fixdate(row['Date'])
            colnum = 0
            for name in fieldnames:
                if name == ISODATE:
                    worksheet.write(rownum, colnum, row[name], dformat)
                else:
                    worksheet.write_string(rownum, colnum, row[name])
                colnum += 1
            rownum += 1
    workbook.close()
    print('Created: {}'.format(xlsxpath))

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _arg = sys.argv[1]
    if _arg.endswith('.csv'):
        _arg = _arg[:-4]
    else:
        print('The input filename must end with ".csv". No action taken.')
        sys.exit(1)
    csvpath = CSVPATH_TEMPLATE.format(_arg)
    xlsxpath = XLSXPATH_TEMPLATE.format(_arg)
    sys.exit(main())
