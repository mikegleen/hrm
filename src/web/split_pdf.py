# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Input is a PDF file specified in the first parameter.
Output is one file in the specified directory per page in the input file. The
name of the output files is <input basename>-page<minor> starting with the
zero-th page, but numbering the files from 001.
"""
import argparse
import os.path
from PyPDF2 import PdfWriter, PdfReader
import sys


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('-o', '--outdir', help='''
    the output directory to contain the split pages. The default is
    the directory containing the input file.
    ''')
    args = parser.parse_args()
    return args


def main(args):
    inputpdf = PdfReader(args.infile)
    indir, basename = os.path.split(args.infile)
    basename = os.path.splitext(basename)[0]  # discard ".pdf"
    outdir = args.outdir if args.outdir else indir
    for i in range(inputpdf.numPages):
        output = PdfWriter()
        output.addPage(inputpdf.getPage(i))
        outfilepath = os.path.join(
            outdir, "{}-{:03}.pdf".format(basename, i + 1))
        print(f'{outfilepath=}')
        output.write(outfilepath)


if __name__ == '__main__':
    assert sys.version_info >= (3, 11)
    main(getargs())
