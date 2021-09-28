"""
Convert all of the .doc format files in the data/transcribe* directories to
html.

Requires libreOffice to be installed and a batch file created containing:
    /Applications/LibreOffice.app/Contents/MacOS/soffice "$@"

In Pycharm, the run config sets the default dir to ~/Documents/hrm.

WARNING: if soffice exits without printing anything, check that you don't have
         libreOffice running in the background.

The following workaround may avoid the above problem:

TODO: add code
 libreoffice "-env:UserInstallation=file:///tmp/LibO_Conversion" --headless --invisible --convert-to csv file.xls


"""

import os
import os.path
import subprocess
import sys
import time

CMD = ('/Users/mlg/bin/soffice --headless --convert-to html {docfile} '
       '--outdir {htmldir}')
DOCDIR = os.path.join('data', 'doc')
HTMLDIR = os.path.join('results', 'html')


def handle_subdir(dirname):
    # handle transcribexxx directory under data/doc
    print(dirname)
    for name in os.listdir(os.path.join(DOCDIR, dirname)):
        # print('    ', name)
        if name.lower().endswith('.doc'):
            docfile = os.path.join(DOCDIR, dirname, name)
            htmldir = os.path.join(HTMLDIR, dirname)
            htmlfile = name[:-4] + '.html'
            htmlfile = os.path.join(htmldir, htmlfile)
            if os.path.exists(htmlfile) and (os.path.getmtime(docfile) <
                                             os.path.getmtime(htmlfile)):
                print('        unmodified: ', name)
                continue
            cmd = CMD.format(docfile=docfile, htmldir=htmldir)
            print('        ', cmd)
            subprocess.check_call(cmd.split())
        else:
            print('        skipping ', name)


def main():
    starttime = time.time()
    for name in os.listdir(DOCDIR):
        if os.path.isdir(os.path.join(DOCDIR, name)):
            handle_subdir(name)
    print('End trans2html. Elapsed time: {:.2f} seconds.'.format(
        time.time() - starttime))
    return 0

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())
