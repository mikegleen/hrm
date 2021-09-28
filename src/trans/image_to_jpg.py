#!/usr/bin/python
"""
Convert an image file to JPEG using the OSX utility sips.

The files must reside in a subdirectory of the directory named as the first
parameter.

To use this script, copy your image file to the "tif" subdirectory of the base
directory.

The script will create a JPEG file in the "jpg" subdirectory.

"""

import os.path
import re
import shutil
import subprocess
import sys

SIPSCMD = 'sips -s format jpeg "{tif_file}" --out "{jpg_file}"'
VERBOS = 0

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    basedir = sys.argv[1]
    tifbase = os.path.join(basedir, 'tif')
    jpgbase = os.path.join(basedir, 'jpg')
    os.makedirs(jpgbase, exist_ok=True)
    for tifname in os.listdir(tifbase):
        tifpath = os.path.join(tifbase, tifname)
        if VERBOS > 0:
            print(tifpath)
        if os.path.isdir(tifpath):
            continue
        leadpart, extension = os.path.splitext(tifname)
        if extension.lower() != '.tif':
            continue
        jpegname = leadpart + '.jpg'
        jpegpath = os.path.join(jpgbase, jpegname)
        if VERBOS > 0:
            print(jpegpath)
        scmd = SIPSCMD.format(tif_file=tifpath, jpg_file=jpegpath)
        if VERBOS > 0:
            print(scmd)
        subprocess.check_call(scmd, shell=True)

