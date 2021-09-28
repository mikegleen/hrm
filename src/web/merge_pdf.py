"""
Merge multiple PDF files into a single file.

The input files must all be in the same directory. The files will be sorted by
filename.

Parameters:
    1. Directory name containing files to be merged.
    2. Output file name.


"""
import os
from PyPDF2 import PdfFileMerger
import sys

VERBOS = 1


def main(indir, outfilename):
    output = PdfFileMerger()
    for pdfname in sorted(os.listdir(indir)):
        pdfpath = os.path.join(indir, pdfname)
        if VERBOS > 0:
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
    assert sys.version_info >= (3, 8)
    main(sys.argv[1], sys.argv[2])

