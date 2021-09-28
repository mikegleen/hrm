# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Input is a PDF file specified in the first parameter.
Output is one file in the specified directory per page in the input file. The
name of the output files is <input basename>-page<minor> starting with the
zero-th page, but numbering the files from 001.
"""
import argparse
import os.path
# noinspection PyProtectedMember
from PyPDF2 import PdfFileWriter, PdfFileReader
import sys


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-o', '--outdir', default='.', help='''
    the output directory to contain the split pages. The default is
    the directory containing the input file.
    ''')
    args = parser.parse_args()
    return args


def main(args):
    inputpdf = PdfFileReader(open(args.infile, "rb"))
    basename = os.path.split(args.infile)[1]
    basename = os.path.splitext(basename)[0]
    for i in range(inputpdf.numPages):
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(i))
        outdirpath = os.path.join(
            args.outdir, "{}-{:03}.pdf".format(basename, i + 1))
        # print(outdirpath)
        with open(outdirpath, "wb") as outputStream:
            output.write(outputStream)


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    main(getargs())
