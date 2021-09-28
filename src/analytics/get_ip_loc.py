# -*- coding: utf-8 -*-  needed because of embedded "£"
"""

"""
import json
import pandas as pd
import subprocess
import sys

TARGET = 'ipinfo.io/{}'
INFILE = '/Users/mlg/pyprj/hrm/data/surveymonkey/ip_addresses.csv'
REPORT = '/Users/mlg/pyprj/hrm/data/surveymonkey/report.json'


def main():
    pass
    infile = open(INFILE)
    reportfile = open(REPORT, 'w')
    for addr in infile:
        addr = addr.strip()
        target = TARGET.format(addr)
        # print(';{};'.format(target))
        completed_process = subprocess.run(['curl', target],
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           universal_newlines=True)
        stdout = json.loads(completed_process.stdout)
        # print(stdout)
        # print(stdout['ip'],stdout['region'])
        val = [stdout[v] for v in 'ip country city'.split()]
        print('{},{},{}'.format(*val))

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())


