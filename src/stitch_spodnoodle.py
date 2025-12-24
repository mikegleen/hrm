"""
    Stitch Spodnoodle images which are scanned in two halves.

    The input directory holds images of the form <accession #>[AB].jpg.

    For example, files JB146A.jpg and JB146B.jpg in the input directory will be merged
    to file JB146.jpg in the output directory.
"""

import argparse
from collections import defaultdict
from colorama import Fore, Style
import cv2 as cv
import os
import re
import sys
import time

IMGEXTS = ('.png', '.jpg', '.jpeg')
MODES = (cv.Stitcher_PANORAMA, cv.Stitcher_SCANS)


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
    the input directory to contain the files to be stitched. These are in the format where
    the first scan filename, not including the extension, has a trailing "A" and the second
    filename has a trailing "B". This conflicts with other usages but for specific data sets
    is convenient. But see option --flagchar.
    ''')
    parser.add_argument('outdir', help='''
    the output directory to contain the stitched files.
    ''')
    parser.add_argument('--dryrun', action='store_true', help='''
    If set, only scan the filenames but do no processing. 
    ''')
    parser.add_argument('--flagchar', help='''
    If specified, then instead of a pattern of [AB] being the part indicator, this character
    will specify the file part to stitch, the part indicated by the digit following the character.
    For example, --flagchar="#" means that a trailing "#1" and "#2" are expected (for two files to stitch)
     Additional files may be specified, up to "#9". The most convenient flag character may vary by operating
     system. Do not use characters used in regular expressions. Known to be safe: "=#%%". Alphabetic letters may be
     used but note that these are case sensitive.''')
    # Note % character escaped but prints normally.
    parser.add_argument('--mdacode', default='LDHRM', help='''
    The MDA code that prepends some accession numbers.
    ''')
    parser.add_argument('--mode',
                        type=int, choices=MODES, default=cv.Stitcher_SCANS,
                        help=f'''Determines configuration of stitcher. The default is `SCANS` ({cv.Stitcher_SCANS})
                             mode suitable for stitching materials under affine transformation, such as scans.
                             Option `PANORAMA` ({cv.Stitcher_PANORAMA}) is suitable for creating photo panoramas.
                             ''')
    parser.add_argument('--overwrite', action='store_true', help='''
    If not set, only the new scans will be processed.
    ''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    args = parser.parse_args()
    return args


def parse_filename(prefix) -> (str, str):
    """
    :param prefix: The filename without the leading path or the extension
    :return: 1. The filename without the part indicator (A or B)
             2. The part indicator
    """
    if prefix.startswith(_args.mdacode):
        # print(f'{prefix=}')
        # matchstring = rf'({_args.mdacode}\.\d+\.\d+(\.\d+)?)[AB]$'
        # print(f'{matchstring=}')
        if flagchar:
            # print(f'{prefix=}, {flagchar=}')
            m = re.match(rf'(?P<base>{_args.mdacode}\.\d+\.\d+(\.\d+)?)(?P<part>{flagchar}\d+)$', prefix)
        else:
            m = re.match(rf'(?P<base>{_args.mdacode}\.\d+\.\d+(\.\d+)?)(?P<part>[AB])$', prefix)
        # print(f'{m=}')
    else:
        if flagchar:
            m = re.match(rf'(?P<base>\D+\d+(\.\d+)?)(?P<part>{flagchar}\d+)$', prefix)
        else:
            m = re.match(rf'(?P<base>\D+\d+(\.\d+)?)(?P<part>[AB])$', prefix)
    if not m:
        return '', ''
    return m['base'], m['part']


def stitch_one(imgs):
    stitcher = cv.Stitcher.create(_args.mode)
    status, pano = stitcher.stitch(imgs)
    if status != cv.Stitcher_OK:
        trace(0, "Can't stitch images, error code = {}", status, color=Fore.RED)
        return None
    return pano


def s(i: int):
    return '' if i == 1 else 's'


def main():
    t1 = time.perf_counter()
    nwritten = 0
    scans = defaultdict(list)
    for filename in sorted(os.listdir(indir)):
        inpath = os.path.join(indir, filename)
        if not os.path.isfile(inpath):
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
        trace(2, 'filename="{}", base="{}", part="{}", extension="{}"', filename, base, part, extension)
        outfile = base + extension
        outpath = os.path.join(_args.outdir, outfile)
        trace(2, 'outpath={}', outpath)
        if not _args.overwrite and os.path.exists(outpath):
            trace(2, 'Skipping already processed scan: {}', outfile)
            continue
        scans[outfile].append(filename)
    trace(2, 'scans = {}', scans)
    if _args.dryrun:
        return

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
        if stitched_img is None:
            trace(1, 'Failed to stitch {}, scans = {}', outfile, scans[outfile], color=Fore.MAGENTA)
            continue
        outpath = os.path.join(outdir, outfile)
        cv.imwrite(outpath, stitched_img)
        nwritten += 1
        trace(2, 'written: {}', outpath)
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
