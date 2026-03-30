"""
Merge multiple PDF files into a single file.

The input files must all be in the same directory. The files will be sorted by
filename.

"""
import argparse
import os
from PyPDF2 import PdfMerger
import sys


def getparser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('indir', help='''The input directory to contain the PDF files.
    ''')
    parser.add_argument('outfile', help='''The output PDF file to contain the merged PDF files.
    ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''Set the verbosity.
The default is 1 which prints summary information.
        ''')
    return parser


def getargs(argv):
    parser = getparser()
    args = parser.parse_args(args=argv[1:])
    return args


def main(indir, outfilename):
    output = PdfMerger()
    for pdfname in sorted(os.listdir(indir)):
        pdfpath = os.path.join(indir, pdfname)
        if _args.verbose > 0:
            print(pdfpath)
        if os.path.isdir(pdfpath):
            continue
        leadpart, extension = os.path.splitext(pdfname)
        if extension.lower() != '.pdf':
            print(f'Ignoring {pdfname}')
            continue
        output.append(pdfpath)
    output.write(outfilename)


if __name__ == '__main__':
    assert sys.version_info >= (3, 9)
    called_from_sphinx = False
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs(sys.argv)
    main(_args.indir, _args.outfile)
