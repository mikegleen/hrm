"""
    Consolidate the weekly report from Google Analytics and produce a CSV file
    with one row for each date.
"""
import os.path
import pandas as pd
import sys


def main(audiencedir):
    files = os.listdir(audiencedir)
    df = pd.DataFrame(columns=['Day', 'Sessions'])
    for filename in files:
        if not filename.endswith('.csv'):
            continue
        filepath = os.path.join(audiencedir, filename)
        tempdf = pd.read_csv(filepath, dtype=str, skiprows=6, header=0,
                             names=['Day', 'Sessions'], dayfirst=True,
                             parse_dates=[0])
        df = df.append(tempdf, ignore_index=True)
    df.dropna(inplace=True)
    df.sort_values('Day', inplace=True)
    df.to_csv(sys.argv[2], index=False)

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    if len(sys.argv) > 2:
        main(sys.argv[1])
    else:
        print('Two parameters needed, the input CSV file and the output'
              ' CSV file.')

