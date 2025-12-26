"""
    Split an image of two drawings vertically.
    The input filename is in one of the formats:
    <accession#>.<item1>&.<item2>#n.jpg --> <accession#>.<item1>#n.jpg and <accession#>.<item2>#n.jpg
    <accession#1>&<accession#2>#n.jpg --> <accession#1>#n.jpg and <accession#2>#n.jpg

    where #n is like #1 or #2. and # is the flag character used by stitch_spodnoodle.py.
"""

import argparse
from colorama import Fore, Style
import cv2 as cv
import os
import re
import sys
import time

from id_utl import expand_idnum

IMGEXTS = ('.png', '.jpg', '.jpeg')



def trace(level, template, *args, color=None):
    if _args.verbose >= level:
        if color:
            print(f'{color}{template.format(*args)}{Style.RESET_ALL}')
        else:
            print(template.format(*args))


def getargs():
    # parser = argparse.ArgumentParser(description='''
    # Stitch the two scans of each Spodnoodle cartoon to a single image.''')
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('indir', help='''
    The input directory holding images to be split.
    ''')
    parser.add_argument('outdir', help='''
    The output directory to contain the split files. ''')
    parser.add_argument('--dryrun', action='store_true', help='''
    If set, only scan the filenames but do no processing. ''')
    parser.add_argument('--flagchar', required=True, help='''
    This character specifies the file part to stitch, the part indicated by the digit following the character.

    For example, --flagchar="#" means that a trailing "#1" and "#2" are expected (for two files to stitch)
     Additional files may be specified, up to "#9". The most convenient flag character may vary by operating
     system. Do not use characters used in regular expressions. Known to be safe: "=#%%". Alphabetic letters may be
     used but note that these are case sensitive.''')
    # Note % character escaped but prints normally.
    parser.add_argument('--mdacode', default='LDHRM', help='''
    The MDA code that prepends some accession numbers. ''')
    parser.add_argument('--overwrite', action='store_true', help='''
    If not set, only the new scans will be processed. ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information. ''')
    parser.add_argument('--y1', nargs=2, type=int, required=True, help='''
    The start and limit pixels for the y-axis of the first image.''')
    parser.add_argument('--y2', nargs=2, type=int, required=True, help='''
    The start and limit pixels for the y-axis of the second image.''')


    args = parser.parse_args()
    return args


def parse_filename(prefix) -> (list, int):
    """
    :param prefix: The filename without the leading path or the extension
    :return: 1. The filename without the part indicator (A or B)
             2. The part indicator
    """
    # Split off the flag string
    #
    m = re.match(rf'(.*)({flagchar}\d)$', prefix)
    if not m:
        return None, 1
    names, flag = m[1], m[2]
    try:
        names = expand_idnum(names)
    except ValueError:
        return None, 2
    if len(names) != 2:
        return None, 3
    return [n + flag for n in names], 0


def s(i: int):
    return '' if i == 1 else 's'


def main():
    t1 = time.perf_counter()
    nwritten = 0
    for filename in sorted(os.listdir(indir)):
        inpath = os.path.join(indir, filename)
        trace(2, 'inpath={}', inpath)
        if not os.path.isfile(inpath):
            trace(1, 'Skipping not file {}', filename, color=Fore.YELLOW)
            continue
        prefix, extension = os.path.splitext(filename)
        if extension.lower() not in IMGEXTS:
            trace(1, 'Skipping not image {}', filename, color=Fore.YELLOW)
            continue
        files, status = parse_filename(prefix)
        if status:
            trace(1, 'Failed parse: {}, error: {}', filename, status, color=Fore.MAGENTA)
            continue
        trace(2, 'input filename="{}", files="{}", extension="{}"', filename, files, extension)
        if _args.dryrun:
            continue
        pixel_y = [_args.y1, _args.y2]
        for n in range(2):
            y_orig, y_lim = pixel_y[n]
            outfile = files[n] + extension
            outpath = os.path.join(_args.outdir, outfile)
            trace(2, 'outpath={}, type={}', outpath, type(outpath))
            if not _args.overwrite and os.path.exists(outpath):
                trace(2, 'Skipping already processed file: {}', outfile)
                continue
            inimg = cv.imread(inpath)
            height, width, _ = inimg.shape
            trace(2,'height={}, width={}', height, width)
            outimg = inimg[y_orig:y_lim, 0:width]
            if _args.dryrun:
                continue
            cv.imwrite(str(outpath), outimg)
            nwritten += 1

    elapsed = time.perf_counter() - t1
    trace(1, f'Elapsed: {elapsed:6.3f} seconds. {nwritten} file{s(nwritten)} written.')

if __name__ == '__main__':
    assert sys.version_info >= (3, 13)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs()
    indir: str = _args.indir
    outdir: str = _args.outdir
    flagchar:str = _args.flagchar
    sys.exit(main())
