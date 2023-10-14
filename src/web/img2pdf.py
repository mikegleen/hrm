# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
    Modified from `trans2pdf.py`

Convert all of the image files in a directory to pdf.

"""

import argparse
import os
import os.path
import sys
import time

from colorama import Style, Fore
from PIL import Image


def trace(level, template, *args, color=None):
    if _args.verbose >= level:
        if color:
            print(f'{color}{template.format(*args)}{Style.RESET_ALL}')
        else:
            print(template.format(*args))


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('indir', help='''
    the input directory to contain the image files.
    ''')
    parser.add_argument('outdir', help='''
    the output directory to contain the PDF files.
    ''')
    args = parser.parse_args()
    return args


def main(indir, outdir):
    starttime = time.time()
    for name in os.listdir(indir):
        subpath = os.path.join(indir, name)
        if os.path.isdir(subpath):
            main(subpath, os.path.join(outdir, name))
            continue
        base, ext = os.path.splitext(name)
        trace(2, 'base={}, ext={}', base, ext)
        if ext.lower() in ('.png', '.jpg', '.jpeg'):
            imgpath = os.path.join(indir, name)
            pdf_file = name[:-len(ext)] + '.pdf'
            pdf_path = os.path.join(outdir, pdf_file)
            trace(2, 'pdf_path={}', pdf_path)
            if os.path.exists(pdf_path) and (os.path.getmtime(imgpath) <
                                             os.path.getmtime(pdf_path)):
                trace(1, '{} unmodified: ', name)
                continue
            image_1 = Image.open(imgpath)
            im_1 = image_1.convert('RGB')
            im_1.save(pdf_path)
        else:
            trace(1, '        skipping {}', name, color=Fore.YELLOW)
    print('End img2pdf. Elapsed time: {:.2f} seconds.'.format(
        time.time() - starttime))
    return 0


if __name__ == '__main__':
    assert sys.version_info >= (3, 11)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs()
    sys.exit(main(_args.indir, _args.outdir))
