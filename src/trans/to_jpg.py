#!/usr/bin/python
"""
Convert a PDF file to JPEG using the OSX utility sips.

There are three modes:
1.  Specify the input and output files.
2.  Specify the directory containing the structure below.
3.  If no parameters are given, the default directory is used.

Directory structure:

base
    - pdf
    - jpg
    - archive

The files must reside in directories with predefined names all within a
predefined base directory (see below).

To use this script, copy your PDF file to the "pdf" subdirectory of the base
directory.

The script will create a JPEG file in the "jpg" subdirectory and move the PDF
file to the "archive" subdirectory.

"""

from __future__ import print_function
import os.path
import re
import shutil
import subprocess
import sys

BASEDIR = '/users/mlg/play/hrm'
SIPSCMD = 'sips -s format jpeg "{pdf_file}" --out "{jpg_file}"'
VERBOS = 0


def one_file(infile, outfile):
    scmd = SIPSCMD.format(pdf_file=infile, jpg_file=outfile)
    if VERBOS > 0:
        print(scmd)
    subprocess.check_call(scmd, shell=True)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        one_file(sys.argv[1], sys.argv[2])
        sys.exit(0)
    elif len(sys.argv) > 1:
        basedir = sys.argv[1]
        if not os.path.isdir(basedir):
            print("Parameter must be a directory.\nNo action taken.")
            sys.exit(1)
    else:
        basedir = BASEDIR

    pdfbase = os.path.join(basedir, 'pdf')
    jpgbase = os.path.join(basedir, 'jpg')
    archivebase = os.path.join(basedir, 'archive')
    for pdfname in os.listdir(pdfbase):
        pdfpath = os.path.join(pdfbase, pdfname)
        if VERBOS > 0:
            print(pdfpath)
        if os.path.isdir(pdfpath):
            continue
        leadpart, extension = os.path.splitext(pdfname)
        if extension.lower() != '.pdf':
            continue
        jpegname = leadpart + '.jpg'
        jpegpath = os.path.join(jpgbase, jpegname)
        if VERBOS > 0:
            print(jpegpath)
        one_file(pdfpath, jpegpath)
        shutil.move(pdfpath, archivebase)
