"""

"""
from PIL import Image
import os.path
import pandas as pd
import pandas.io.excel as ex
import sys
import matplotlib.pyplot as plt


HEADING = ['Title', 'Periodical', 'Date', 'Page', 'File', 'ISODate']
WORKBOOK = os.path.join('results', 'whr-cartoons.xlsx')
BARPLOT = os.path.join('results', 'plots', 'barplot.png')


def main():
    cartoons = ex.read_excel(WORKBOOK, 'Sheet1')
    cartoons.dropna(inplace=True)
    # cartoons['ISODate'] = pd.to_datetime(cartoons.ISODate)
    cartoons['Year'] = cartoons.ISODate.dt.year.astype('int')
    c = cartoons.groupby('Year').count()
    p = c.ISODate.plot(kind='bar', legend=False)
    fig = p.get_figure()
    fig.savefig(BARPLOT)
    Image.open(BARPLOT).save(BARPLOT[:-4] + '.jpg', 'JPEG')
    print('Exit plot.')

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())
