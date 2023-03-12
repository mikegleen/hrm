import argparse
import codecs
import csv
import json
import sys


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='''
    the input file in JSON format
    ''')
    parser.add_argument('outfile', help='''
    the output file in pretty JSON
    ''')
    args = parser.parse_args()
    return args


def main():
    obj = json.load(open(_args.infile))
    outf = codecs.open(_args.outfile, 'w', 'utf-8-sig')
    outcsv = csv.writer(outf)
    print('Number of cards:', len(obj['cards']))
    for card in obj['cards']:
        row = [card['name'], card['desc']]
        outcsv.writerow(row)


if __name__ == '__main__':
    assert sys.version_info >= (3, 6)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs()
    main()
