"""
    Stitch Spodnoodle images which are scanned in two halves.

    The input directory holds images of the form <accession #>[AB]
"""

import argparse
from collections import defaultdict
from colorama import Fore, Style
import cv2 as cv
import os
import re
import sys

IMGEXTS = ('.png', '.jpg', '.jpeg')


def trace(level, template, *args, color=None):
    if _args.verbose >= level:
        if color:
            print(f'{color}{template.format(*args)}{Style.RESET_ALL}')
        else:
            print(template.format(*args))


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('indir', help='''
    the input directory to contain the files to be stitched.
    ''')
    parser.add_argument('outdir', help='''
    the output directory to contain the stitched files.
    ''')
    parser.add_argument('-m', '--mdacode', default='LDHRM', help='''
    The MDA code that prepends some accession numbers.
    ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    args = parser.parse_args()
    return args


def parse_filename(prefix) -> (str, str):
    """

    :param prefix: The filename without the leading path
    :return: 1. The filename without the part indicator (A or B)
             2. The part indicator
             3. The filename extension
    """
    if prefix.startswith(_args.mdacode):
        # print(f'{prefix=}')
        # matchstring = rf'({_args.mdacode}\.\d+\.\d+(\.\d+)?)[AB]$'
        # print(f'{matchstring=}')
        m = re.match(rf'(?P<base>{_args.mdacode}\.\d+\.\d+(\.\d+)?)(?P<part>[AB])$', prefix)
        # print(f'{m=}')
    else:
        m = re.match(rf'(?P<base>\D+\d+(\.\d+)?)(?P<part>[AB])$', prefix)
    if not m:
        return '', ''
    return m['base'], m['part']


def stitch_one(imgs):
    stitcher = cv.Stitcher.create(cv.Stitcher_PANORAMA)
    status, pano = stitcher.stitch(imgs)

    if status != cv.Stitcher_OK:
        trace(0, "Can't stitch images, error code = {}", status, color=Fore.RED)
        sys.exit(-1)
    return pano


def main():
    scans    = defaultdict(list)
    for filename in os.listdir(indir):
        path = os.path.join(indir, filename)
        if not os.path.isfile(path):
            trace(1, 'Skipping not file {}', filename, color=Fore.YELLOW)
            continue
        prefix, extension = os.path.splitext(filename)
        if extension.lower() not in IMGEXTS:
            trace(1, 'Skipping not image {}', filename, color=Fore.YELLOW)
            continue
        base, part = parse_filename(prefix)
        if not base:
            trace(1, 'Failed parse: {}', filename, color=Fore.MAGENTA)
            continue
        trace(2, 'filename={}, base={}, part={}, extension={}', filename, base, part, extension)
        outfile = base + extension
        outpath = os.path.join(_args.outdir, outfile)
        trace(2, 'outpath={}', outpath)
        scans[outfile].append(filename)
    trace(2, 'scans = {}', scans)

    for outfile in scans:
        infiles = scans[outfile]
        if len(infiles) != 2:
            trace(1, 'Skipping – only one file found for: {}', outfile, color=Fore.MAGENTA)
            continue
        imgs = []
        for infile in infiles:
            inpath: str = os.path.join(indir, infile)
            img = cv.imread(inpath)
            if img is None:
                trace(0, "can't read image {}", infile, color= Fore.RED)
                sys.exit(-1)
            imgs.append(img)
        stitched_img = stitch_one(imgs)
        outpath = os.path.join(outdir, outfile)
        cv.imwrite(outpath, stitched_img)
        trace(2, 'written: {}', outpath)

if __name__ == '__main__':
    assert sys.version_info >= (3, 13)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs()
    indir: str = _args.indir
    outdir: str = _args.outdir
    sys.exit(main())
