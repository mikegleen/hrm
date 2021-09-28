"""
    Search the subscribed_members_export...csv file from MailChimp for
    duplicate names and report the corresponding email addresses.
"""

import sys
import csv


def main(csvfilename):
    namedict = {}
    withname, noname = 0, 0
    with open(csvfilename, newline='') as csvfile:
        chimpreader = csv.reader(csvfile)
        next(chimpreader)  # Skip heading
        for row in chimpreader:
            email, firstname, lastname = [x.strip() for x in row[:3]]
            fullname = firstname + '_' + lastname
            if fullname == '_':
                noname += 1
                continue
            if fullname in namedict:
                namedict[fullname].append(email)
            else:
                withname += 1
                namedict[fullname] = [email]
        for fullname in namedict:
            if len(namedict[fullname]) > 1:
                print(fullname.replace('_', ' '),)
                for email in namedict[fullname]:
                    print('  ', email)
        print("noname", noname)
        print('withname', withname)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('One parameter needed, the input CSV file.')

