"""
    Search the subscribed_members_export...csv file from MailChimp for
    suspected redundant email addresses with no corresponding first/last names
    and report the affected email addresses.
"""

import sys
import csv


def main(csvfilename):
    namedict = {}
    with open(csvfilename, newline='') as csvfile:
        chimpreader = csv.reader(csvfile)
        next(chimpreader)  # Skip heading
        for row in chimpreader:
            email, firstname, lastname = [x.strip() for x in row[:3]]
            fullname = firstname + '_' + lastname
            if fullname != '_':  # Skip records with first/last names
                continue
            emailname = email.split('@')[0]
            if emailname in namedict:
                namedict[emailname].append(email)
            else:
                namedict[emailname] = [email]
        for emailname in namedict:
            if len(namedict[emailname]) > 1:
                print(emailname)
                for email in namedict[emailname]:
                    print('  ', email)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('One parameter needed, the input CSV file.')


