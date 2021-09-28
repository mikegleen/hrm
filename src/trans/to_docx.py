"""

"""
import docx
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
import os.path
import pandas as pd
import sys
import time

HRMDIR = os.path.join('/', 'Users', 'mlg', 'Documents', 'hrm')
TEMPLATEPATH = os.path.join(HRMDIR, 'doc', 'hr_template.docx')
RESULTSDIR = os.path.join(HRMDIR, 'results')
XLSXPATH = os.path.join(RESULTSDIR, 'whr-cartoons.xlsx')
DOCXPATH = os.path.join(RESULTSDIR, 'docx', 'whr-cartoons.docx')


def putrow(table, dfrow):
    tabrow = table.add_row().cells
    tabrow[0].text = dfrow[1]  # Title
    tabrow[1].text = dfrow[2]  # Periodical
    text = str(dfrow[3])  # Date
    tabrow[2].text = text if text != 'nan' else ''
    text = str(dfrow[4])  # Page
    tabrow[3].text = text if text != 'nan' else ''


def main():
    starttime = time.time()
    df = pd.read_excel(XLSXPATH)
    document = Document(TEMPLATEPATH)
    table = document.tables[0]
    print(WD_STYLE_TYPE.PARAGRAPH)
    table.style = docx.styles.styles.Styles(WD_STYLE_TYPE.PARAGRAPH)
    table.style.paragraph_format.keep_together = True
    for row in df.itertuples():
        putrow(table, row)
    document.save(DOCXPATH)
    print('End to_docx. Elapsed time: {:.2f} seconds.'.
          format(time.time() - starttime))

if __name__ == '__main__':
    if sys.version_info.major < 3:
        raise ImportError('requires Python 3')
    sys.exit(main())


