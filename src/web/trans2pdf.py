# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Convert all of the .doc or .docx format files in a directory to pdf.

Requires libreOffice to be installed and a batch file created containing:
    /Applications/LibreOffice.app/Contents/MacOS/soffice "$@"

WARNING: if soffice exits without printing anything, check that you don't have
         libreOffice running in the background.
"""

import argparse
import os
import os.path
import subprocess
import sys
import time

CMD = ('/Users/mlg/bin/soffice;--headless;--convert-to;pdf;{docfile};'
       '--outdir;{pdfdir}')
DOCDIR = os.path.join('data', 'doc')
PDFDIR = os.path.join('results', 'pdf')


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('indir', default=DOCDIR, help='''
    the input directory to contain the doc files.
    ''')
    parser.add_argument('outdir', default=PDFDIR, help='''
    the output directory to contain the PDF files.
    ''')
    args = parser.parse_args()
    return args


def main():
    starttime = time.time()
    for name in os.listdir(_args.indir):
        base, ext = os.path.splitext(name)
        if ext.lower() in ('.doc', '.docx'):
            docfile = os.path.join(_args.indir, name)
            pdf_file = name[:-len(ext)] + '.pdf'
            pdf_file = os.path.join(_args.outdir, pdf_file)
            if os.path.exists(pdf_file) and (os.path.getmtime(docfile) <
                                             os.path.getmtime(pdf_file)):
                print('        unmodified: ', name)
                continue
            cmd = CMD.format(docfile=docfile, pdfdir=_args.outdir)
            print('        ', cmd)
            subprocess.check_call(cmd.split(';'))
        else:
            print('        skipping ', name)
    print('End trans2pdf. Elapsed time: {:.2f} seconds.'.format(
        time.time() - starttime))
    return 0


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    _args = getargs()
    sys.exit(main())

