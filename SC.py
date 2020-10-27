import bs4 as bs  # webscraper
import urllib.request
import requests  # downloads files
import re  # regex
import pprint as pp  # prettyprint
import os  # for finding current working directory
from scraper import Scraper

tempPdfs = os.path.join((os.getcwd()), 'temp')  # string for file path to Temp folder
print('Files will be saved in ', tempPdfs)

source = urllib.request.urlopen('https://www.national-lottery.co.uk/games/gamestore/scratchcards').read()
soup = bs.BeautifulSoup(source, 'lxml')
table = soup.table

table_rows = table.find_all('tr')  # table_rows list, not standard list type. BS4 element result set.
SClist = []  # ScratchCard List of lists. All results will end up here.
sc_objects = []
for tr in table_rows[1:]:  # for tableresults in tablerows. Skip first item.
    td = tr.find_all('td')  # tabledata in tablerow
    row = [i.text for i in td]  # row = make list of text in table row (BSlist, not normal)

    """IMAGE & PDF """
    image_pdf = tr.find_all("a", href=True)
    row.append(str(image_pdf[0]))  # image
    row.append(str(image_pdf[1]))  # pdf

    """ STORE DATA """
    SClist.append(row)                  # add to SClist (normal list)
    sc_objects.append(Scraper(row))     # list of objects
    print(row)


rowCount = int(len(table_rows)) - 1  # rowCount is the number of rows, minus 1 for title

