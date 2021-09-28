# -*- coding: utf-8 -*-
"""
    Compare the workshop email list to the list of emails already known to
    MailChimp.
    
    Create a CSV file with the existing email addresses removed from the
    original list. Save this file in a directory named "results" under
    the directory containing the input workshop list.
    
    The output filename is of the format "workshop_emails_%Y%m%d-%H%M%S.csv".
"""
from collections import namedtuple
import datetime
import csv
import os
import pandas.io.excel as ex
import sys

TITLES = 'mr mrs miss dr'.split()

Entry = namedtuple('Entry', 'email_address surname firstname'.split())


def prune(wdict, mcdir, mcfilename):
    """
    
    :param wdict: dictionary of email addresses from the workshop excel file
    :param mcdir: the directory containing file mcfilename
    :param mcfilename: a MailChimp CSV file containing email addresses that
           we must delete from wdir
    :return: None
    """
    # Extract preamble from the filename. For example:
    # subscribed_members_export_00d72831eb.csv -> subscribed
    preamble = mcfilename.split('_')[0]
    notdups, dups = 0, 0
    mcpath = os.path.join(mcdir, mcfilename)
    with open(mcpath, newline='') as csvfile:
        chimpreader = csv.reader(csvfile)
        next(chimpreader)
        for row in chimpreader:
            email = row[0].strip()
            if email in wdict:
                dups += 1
                del wdict[email]
                # print('  del:', email, ',', preamble)
    print(preamble, 'dups found:', dups)


def make_entry(row):
    surname = row.surname.title()  # capitalize names
    first_name = row.first_name.title()
    if len(surname) == 1:
        surname = ''
    if len(first_name) == 1:
        first_name = ''
    splitname = first_name.split()
    if len(splitname) and splitname[0].lower() in TITLES:
        first_name = ''

    return Entry(row.email_address, surname, first_name)


def main(workshop, mailchimpdir):
    if not os.path.isdir(mailchimpdir):
        print(mailchimpdir, 'must be a directory.')
        return
    wdict = {}
    wdf = ex.read_excel(workshop, 'Sheet1', parse_cols=(0, 1, 2))
    wdf.rename(columns={'Surname': 'surname',
                        'First name': 'first_name',
                        'Email address': 'email_address'},
               inplace=True)
    wdf.dropna(subset=['email_address'], inplace=True)
    wdf.fillna('', inplace=True)
    for c in wdf.columns:
        wdf[c] = wdf[c].str.strip()
    for row in wdf.itertuples():
        wdict[row.email_address] = make_entry(row)
    # print(wdict)
    for filename in os.listdir(mailchimpdir):
        if not filename.endswith('.csv'):
            continue
        prune(wdict, mailchimpdir, filename)
    print('Workshop emails:', len(wdict))
    outdir = os.path.dirname(workshop)
    outdir = os.path.join(outdir, 'results')
    os.makedirs(outdir, exist_ok=True)
    outfilename = _starttime.strftime("workshop_emails_%Y%m%d-%H%M%S.csv")
    outpath = os.path.join(outdir, outfilename)
    with open(outpath, 'w', newline='') as outfile:
        outwriter = csv.writer(outfile)
        outwriter.writerow('email surname firstname'.split())
        for k in sorted(wdict):
            outwriter.writerow(wdict[k])

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _starttime = datetime.datetime.today()

    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print('Two parameters needed, the workshop XLSX file and the'
              ' mailchimp CSV directory.')
