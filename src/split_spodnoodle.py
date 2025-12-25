"""
    Split an image of two drawings vertically.
    The input filename is in one of the formats:
    <accession#>.<item1>&.<item2>#n.jpg --> <accession#>.<item1>#n.jpg and <accession#>.<item2>#n.jpg
    <accession#1>&<accession#2>#n.jpg --> <accession#1>#n.jpg and <accession#2>#n.jpg

    where #n is like #1 or #2. and # is the flag character used by stitch_spodnoodle.py.
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

def _expand_one_idnum(idstr: str) -> list[str]:
    jlist = []
    idstr = ''.join(idstr.split())  # remove all whitespace
    if '-' in idstr or '/' in idstr:  # if ID is actually a range like JB021-23
        if '&' in idstr:
            raise ValueError(f'Bad accession number list: cannot contain both'
                             f' "-" and "&": "{idstr}"')
        if m := re.match(r'''(.+?)  # prefix like "JB" or "LDHRM.2024."
                             (\d+)  # number up to the separator
                             [-/]   # the separator can be "-" or "/"
                             (.*?)  # possibly a prefix on the second part
                             (\d+)$ # the trailing number
                             ''', idstr, flags=re.VERBOSE):
            prefix, num1, num2, lenvariablepart = _splitid(idstr, m)
            try:
                for suffix in range(num1, num2 + 1):
                    newidnum = f'{prefix}{suffix:0{lenvariablepart}}'
                    jlist.append(newidnum)
            except ValueError:
                raise ValueError(f'Bad accession number, contains "-" but not '
                                 f'well formed: {m.groups()}')
        else:
            raise ValueError('Bad accession number, failed pattern match:', idstr)
    elif '&' in idstr:
        parts = idstr.split('&')
        head = parts[0]
        jlist.append(head)
        m = re.match(r'(.+?)(\d+)$', head)
        # prefix will be everything up to the trailing number. So for:
        #   JB001 -> JB
        #   LDHRM.2023.1 -> LDHRM.2023.
        prefix = m[1]
        for tail in parts[1:]:
            if not tail.isnumeric():
                raise ValueError(f'Extension numbers must be numeric: "{idstr}"')
            jlist.append(prefix + tail)

    else:
        # It's just a single accession number.
        jlist.append(idstr)
    return jlist


def expand_idnum(idnumstr: str) -> list[str]:
    """
    Expand an idnumstr to a list of idnums.
    :param idnumstr: (See expand_one_idnum for the definition of idstr)
        idnumstr ::= idstr | idnumstr,idstr
    :return: list of idnums
    """
    idstrlist = idnumstr.split(',')
    rtnlist = []
    for idstr in idstrlist:
        # _expand_one_idnum returns a list. Append the members of that list.
        rtnlist += _expand_one_idnum(idstr)
    return rtnlist


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


def parse_filename(prefix) -> (str, str):
    """
    :param prefix: The filename without the leading path or the extension
    :return: 1. The filename without the part indicator (A or B)
             2. The part indicator
    """
    err = 0
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
