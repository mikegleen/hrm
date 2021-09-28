# -*- coding: utf-8 -*-
"""
    Zip folder whose names are in the form yyyy-mm-dd. Only zip folders that
    are older than 180 days.

"""

import datetime
import os
import shutil

DRYRUN = False
DAYS_TO_KEEP = 180
EVENTS_PATH = ('/Users/mlg/Library/Mobile Documents/' +
               'com~apple~CloudDocs/hrm/events')
DATELEN = len('yyyy-mm-dd')
keepdate = datetime.date.today() - datetime.timedelta(days=DAYS_TO_KEEP)
dirlist = os.listdir(EVENTS_PATH)

for name in sorted(dirlist):
    zpath = os.path.join(EVENTS_PATH, name)
    if not os.path.isdir(zpath):
        continue
    try:
        namedate = datetime.datetime.strptime(name[:DATELEN], '%Y-%m-%d').date()
    except ValueError:
        continue
    if namedate >= keepdate:
        continue
    zname = name + '.zip'
    if zname in dirlist:
        print(f'Not overwriting {zname}')
        continue
    print(f'Compressing {zpath}')
    if DRYRUN:
        continue
    shutil.make_archive(zpath, 'zip', zpath)
