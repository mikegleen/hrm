"""
Read each of the HTML files created by trans2html.py, extract the table data,
and create a CSV file with a column appended containing the name of the source
file (minus the trailing .html)

If one file is specified on the command line, it is expected to be in
results/html and the output will be in results/csv. This file must be specified
with a trailing ".html".

If nothing is specified on the command line, each subdirectory in results/html
is processed in turn and corresponding subdirectories in results/csv are
created.
"""

from bs4 import BeautifulSoup as Bs
import collections
import csv
import os.path
import sys

CSVDIR = os.path.join('results', 'csv')
CSVFILENAME = 'merged.csv'
HTMLDIR = os.path.join('results', 'html')
TRACE_ON = 1
HEADING = ['Title', 'Periodical', 'Date', 'Page', 'File']


def trace(template, *args):
    if TRACE_ON:
        print(template.format(*args))

# print(len(rows), rows[2])


def handle_one_row(row):
    csvrow = []
    details = row.find_all('td')
    for td in details:
        paras = td.find_all('p')
        detail = ''
        for para in paras:
            # replace whitespace with a single space
            text = ' '.join(para.text.split())
            detail += text + '\n'
        if not detail:  # if there was no <p> tag
            detail = td.text
        detail = detail.strip()  # remove trailing NL
        csvrow.append(detail)
    return csvrow


def handle_one_file(outcsv, htmlpath, name):
    global rowcount
    filepath = os.path.join(htmlpath, name)
    trace('        input: {}', filepath)
    htmlfile = open(filepath)
    soup = Bs(htmlfile, 'html.parser')  # , 'html5lib')
    table = soup.find('table')
    rows = table.find_all('tr')

    for row in rows:
        outrow = handle_one_row(row)
        # ignore empty rows and title rows
        if len(outrow) > 3 and outrow[0] and outrow[1] != 'Periodical':
            outrow.append(name[:-5])  # all but trailing ".html"
            outcsv.writerow(outrow)
            rowcount += 1
    htmlfile.close()


def handle_subdir(outcsv, dirname):
    # handle transcribexxx directory under results/html
    html_sub_path = os.path.join(HTMLDIR, dirname)
    trace('{}', html_sub_path)
    for name in sorted(os.listdir(html_sub_path)):
        trace('    {}', name)
        if name.lower().endswith('.html'):
            handle_one_file(outcsv, html_sub_path, name)
        else:
            trace('        skipping {}', name)


def opencsvwriter(filename):
    global csvpath
    csvpath = os.path.join(CSVDIR, filename)
    csvfile = open(csvpath, 'w', newline='')
    outcsv = csv.writer(csvfile, delimiter='|')
    outcsv.writerow(HEADING)
    trace('Output: {}', csvpath)
    return outcsv


def main():
    global rowcount
    outcsv = opencsvwriter(CSVFILENAME)
    for name in sorted(os.listdir(HTMLDIR)):
        if os.path.isdir(os.path.join(HTMLDIR, name)):
            handle_subdir(outcsv, name)


def one_file():
    csvname = sys.argv[1][:-5] + '.csv'
    outcsv = opencsvwriter(csvname)
    handle_one_file(outcsv, HTMLDIR, sys.argv[1])


if __name__ == '__main__':
    csvpath = ''
    rowcount = 0
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) < 2:
        main()
    else:
        one_file()
    print('\nEnd html2csv. {} rows written to {}'.
          format(rowcount, os.path.abspath(csvpath)))
