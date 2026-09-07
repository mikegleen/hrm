import argparse
from colorama import Fore, Style
import os.path
import re
import sys
from PIL import Image

sys.path.insert(1, '/Users/mlg/pyprj/hrm/modes/src')

from utl import normalize  # noqa
# print(sys.path)
# sys.exit()

DESCRIPTION = """
    Iterate over a folder and its sub-folders.

    If a file is .tif or .bmp format, and if the filename is or can be parsed as
    an accession number, copy it to a destination folder, converting to JPEG.

"""

def trace(level, template, *args, color=None):
    if _args.verbose >= level:
        if color:
            print(f'{color}{template.format(*args)}{Style.RESET_ALL}')
        else:
            print(template.format(*args))


def getparser():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-i', '--indir', help='''
        The folder containing files and sub-folders to search.''')
    parser.add_argument('-o', '--outdir', required=True, help='''
        Folder to contain the output JPEG files''')
    parser.add_argument('--dryrun', action='store_true', help='''
        If not set, only the new scans will be processed. ''')
    parser.add_argument('-q', '--quality', default=95, type=int, help=f'''
        Specify the output quality. The default is 95''')
    parser.add_argument('-v', '--verbose', type=int, default=1, help='''
        Set the verbosity. The default is 1 which prints summary information.
        ''')
    return parser


def getargs(argv):
    parser = getparser()
    args = parser.parse_args(args=argv[1:])
    return args


def one_file(indir, filename):
    name, ext = os.path.splitext(filename)
    filepath = os.path.join(indir, filename)
    if not ext.lower() in ('.tif', '.bmp'):
        trace(1, f'skipping {filepath}', color=Fore.YELLOW)
        return
    m = re.match(r'([a-zA-Z0-9]+)?[_ ].*', name)
    if m:
        name = m[1]
    newfilename = name + '.jpg'
    newfilepath = os.path.join(_args.outdir, newfilename)
    trace(2, f'{filename} -> {newfilepath}')
    if name in in_outdir:
        trace(1, f'in outdir: {name}, {filename=}', color=Fore.RED)
        return
    if name in found:
        trace(1, f'duplicate: {name}, {filename=}', color=Fore.RED)
        return
    found.add(name)
    if _args.dryrun:
        return
    img = Image.open(filepath)
    rgb_img = img.convert('RGB')
    rgb_img.save(newfilepath, quality=_args.quality)

def one_dir(indir):
    trace(1, 'folder = {}', indir, color=Fore.MAGENTA)
    for filename in os.listdir(indir):
        filepath = os.path.join(indir, filename)
        if os.path.isdir(filepath):
            one_dir(filepath)  # recursively walk subdirectory
        else:
            one_file(indir, filename)


def main():
    if not os.path.isdir(_args.indir):
        trace(1, f'{_args.indir} is not a directory. Aborting.', color=Fore.RED)
        sys.exit(-1)
    if not os.path.isdir(_args.outdir):
        trace(1, f'{_args.outdir} is not a directory. Aborting.', color=Fore.RED)
        sys.exit(-1)
    for filename in os.listdir(_args.outdir):
        root, ext = os.path.splitext(filename)
        in_outdir.add(root)
    one_dir(_args.indir)


if __name__ == '__main__':
    assert sys.version_info >= (3, 13)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    _args = getargs(sys.argv)
    in_outdir = set()
    found = set()
    main()