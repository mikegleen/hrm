"""
Input:  merged.csv (hard coded)
        file in arg[1]
Output: updated.csv (hard coded)

Read the CSV file merged from the individual page .doc files by
the tool chain [*.doc] --trans2html--> [*.html] --html2csv --> [merged.csv]
and create a dictionary using the Publication, Date, and Page fields as the
key, checking for duplicates.

Read the CSV file (arg[1]) created from the manually edited doc file and create
a similar dictionary (called "edited").

Compare each entry in the merged .csv file with the corresponding entry in the
edited .csv file.  Display the mismatches of the 'Title' fields.
There will be many of these as this is what has been corrected. Also check for
any missing records (in either direction).

"""
import argparse
import collections
import copy
import csv
import os.path
import sys
import time

TRACE_ON = True
# RESULTSDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm', 'results')
# RESULTSDIR = os.path.join('/', 'Users', 'mlg', 'pyprj', 'hrm', 'results')
RESULTSDIR = os.path.join('.', 'results')
CSVDIR = os.path.join(RESULTSDIR, 'csv')
'''
The following file was produced by html2csv.py (see the description above).
'''
MERGEDPATH = os.path.join(CSVDIR, 'merged.csv')
'''
The following file is the corrected output.
'''
UPDATEDPATH = os.path.join(CSVDIR, 'updated.csv')
"""
The following two files will hold paired records whose Title field mismatch.
These can be diff-ed to see what was changed.
"""
FINALCORRPATH = os.path.join(CSVDIR, 'finalcorr.csv')
MERGEDCORRPATH = os.path.join(CSVDIR, 'mergedcorr.csv')

HEADING = ['Title', 'Periodical', 'Date', 'Page', 'File']


Rowtuple = collections.namedtuple('Rowtuple', ('Seq',) + tuple(HEADING))


def trace(template, *args):
    if TRACE_ON:
        print(template.format(*args))


def opencsvreader(csvpath):
    csvfile = open(csvpath)
    incsv = csv.reader(csvfile, delimiter='|')
    trace('Input: {}', csvpath)
    return incsv


def opencsvwriter(csvpath):
    csvfile = open(csvpath, 'w', newline='')
    outcsv = csv.writer(csvfile, delimiter='|')
    trace('Output: {}', csvpath)
    return outcsv


def build_dict(name, path):
    seq = 0
    reader = opencsvreader(path)
    csvdict = collections.OrderedDict()
    for row in reader:
        seq += 1
        nrow = Rowtuple(seq, *row)
        key = (nrow.Periodical, nrow.Date, nrow.Page)
        if key in csvdict:
            old = csvdict[key]
            print('------------\nDuplicate: {} seq {}, {}'.
                  format(name, old.Seq, seq))
            print(old)
            print('----')
            print(nrow)
        else:
            csvdict[key] = nrow
    trace('Merged: {} rows processed. Dict len: {}', seq, len(csvdict))
    return csvdict


def compare_dicts(fromgoeff, original):
    corrections = 0
    errors = 0
    corrected = copy.copy(fromgoeff)
    mcorr_writer = opencsvwriter(MERGEDCORRPATH)
    fcorr_writer = opencsvwriter(FINALCORRPATH)
    updated_writer = opencsvwriter(UPDATEDPATH)

    for key, row in original.items():
        if key in corrected:
            if row.Title != corrected[key].Title:
                # strip leading row # and trailing filename
                mcorr_writer.writerow(row[1:-1])
                fcorr_writer.writerow(fromgoeff[key][:-1])
                row = list(row)
                row[1] = fromgoeff[key][1]
                corrections += 1
            del corrected[key]
            updated_writer.writerow(row[1:])  # strip off leading row number
        else:
            print('---- original not found:    ', row)
            errors += 1
    print('{} not found in original. {} extras in original:'.
          format(errors, len(corrected)))
    for key, row in corrected.items():
        print('    extra: ', row)
        errors += 1
    return corrections, errors


def get_args():
    parser = argparse.ArgumentParser(description='''
    Apply the manually edited texts to the records created from the
    individual CSV files obtained from the one-per-page DOC files.''')
    parser.add_argument('-e', '--edited', help='''This file contains the
    merged original records except some were manually updated by the
    proofreader.  The file named here must be in directory {}'''.
                        format(CSVDIR))
    args = parser.parse_args()
    return args


def main(editedpath):
    starttime = time.time()
    merged = build_dict('merged', MERGEDPATH)
    edited = build_dict('edited', editedpath)
    corrections, errors = compare_dicts(edited, merged)
    print('End correct_text. Elapsed time: {:.2f} seconds.'.
          format(time.time() - starttime))
    print('{} corrections.'.format(corrections))
    return 1 if errors else 0

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = get_args()
    _editedpath = os.path.join(CSVDIR, _args.edited)
    sys.exit(main(_editedpath))
