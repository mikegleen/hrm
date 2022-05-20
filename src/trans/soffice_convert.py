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

CMD = ('/Users/mlg/bin/soffice --headless --convert-to {format} {docfile} '
       '--outdir {outdir}')


def main():
    starttime = time.time()
    for name in os.listdir(args.indir):
        docpath = os.path.join(args.indir, name)
        if os.path.isdir(docpath):
            continue
        root, ext = os.path.splitext(name)
        if ext.lower() in ('.doc', '.docx'):
            outfile = root + args.extension
            outpath = os.path.join(args.outdir, outfile)
            if os.path.exists(outpath) and (os.path.getmtime(docpath) <
                                            os.path.getmtime(outpath)):
                print('        unmodified: ', name)
                continue
            if ' ' in name:
                newname = name.replace(' ', '_')
                newpath = os.path.join(args.indir, newname)
                os.rename(docpath, newpath)
                docpath = newpath
            cmd = CMD.format(docfile=docpath, outdir=args.outdir,
                             format=args.format)
            print('        ', cmd)
            subprocess.check_call(cmd.split())
        else:
            print('        skipping ', name)
    print('End trans2html. Elapsed time: {:.2f} seconds.'.format(
        time.time() - starttime))
    return 0


def getparser():
    parser = argparse.ArgumentParser(description='''
    Convert all of the various format files in the data/transcribe* directories to
    the specified format.
    ''')
    parser.add_argument('indir', help='''
        The directory containing files to convert''')
    parser.add_argument('outdir',  help='''
        The directory to contain the converted files.''')
    parser.add_argument('format',  help='''
        The format to convert files to.''')
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
    return arguments


if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    args = getargs(sys.argv)
    sys.exit(main())
