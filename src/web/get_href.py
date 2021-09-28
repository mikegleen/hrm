# -*- coding: utf-8 -*-  needed because of embedded "£"
"""
Iterate over "a" tags in an html file and scrape the files named to the local
machine.
"""

from bs4 import BeautifulSoup as Bs
import os.path
import requests

DATA = os.path.join('data', 'volunteer.html')
TARGETDIR = 'fromweb'

htmlfile = open(DATA)
soup = Bs(htmlfile, 'html.parser')  # , 'html5lib')
anchor = soup.find_all('a')
for tag in anchor:
    href = tag['href']
    # print('href', href)
    basename = os.path.basename(href)
    # print('basename', basename)
    response = requests.get(href)
    with open(os.path.join(TARGETDIR, basename), 'wb') as handle:
        handle.write(response.content)

