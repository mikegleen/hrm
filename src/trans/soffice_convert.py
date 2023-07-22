"""
Convert all of the various format files in a directory to
the specified format.

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

CMD = ('/Users/mlg/bin/soffice --headless --convert-to {format} {infile} '
       '--outdir {outdir}')


def main():
    starttime = time.time()
    for name in os.listdir(args.indir):
        inpath = os.path.join(args.indir, name)
        if os.path.isdir(inpath):
            continue
        root, ext = os.path.splitext(name)
        if ext.lower() not in args.filter:
            print('******* skipping ', name)
            continue
        outfile = root + args.extension
        outpath = os.path.join(args.outdir, outfile)
        if os.path.exists(outpath) and (os.path.getmtime(inpath) <
                                        os.path.getmtime(outpath)):
            print('******* unmodified: ', name)
            continue
        if ' ' in name:
            newname = name.replace(' ', '_')
            newpath = os.path.join(args.indir, newname)
            os.rename(inpath, newpath)
            inpath = newpath
        cmd = CMD.format(infile=inpath, outdir=args.outdir,
                         format=args.format)
        print('        ', cmd)
        subprocess.check_call(cmd.split())
    print('End soffice_convert. Elapsed time: {:.2f} seconds.'.format(
          time.time() - starttime))
    return 0


def getparser():
    parser = argparse.ArgumentParser(description='''
    Convertthe files in the input directory whose extensions match the filter
    criteria to the specified format.
    ''')
    parser.add_argument('indir', help='''
        The directory containing files to convert''')
    parser.add_argument('outdir',  help='''
        The directory to contain the converted files.''')
    parser.add_argument('format',  help='''
        The format to convert files to.''')
    parser.add_argument('-f', '--filter', action='append', help='''
        The extention of allowed input files. The default value is ['.doc', '.docx'].
        Multiple --filter options may be specified.''')
    parser.add_argument('-e', '--extension',  help='''
        The extension to be added to the output files. If omitted, the format
        value is used.''')
    return parser


def getargs(argv):
    parser = getparser()
    arguments = parser.parse_args()
    if not arguments.extension:
        arguments.extension = arguments.format
    if not arguments.extension.startswith('.'):
        arguments.extension = '.' + arguments.extension
    if not arguments.filter:
        arguments.filter = ['.doc', '.docx']
    arguments.filter = [(f if f.startswith('.') else '.' + f).lower()
                        for f in arguments.filter]
    return arguments


if __name__ == '__main__':
    assert sys.version_info >= (3, 6)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = getargs(sys.argv)
    sys.exit(main())
