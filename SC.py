import bs4 as bs  # webscraper
import urllib.request
import requests  # downloads files
import re  # regex
import pprint as pp  # prettyprint
import os  # for finding current working directory
from scratchcards import Scratchcards
from Logger import SC_Logfile

class Scraper:
    def __init__(self):
        self.temp_pdfs = os.path.join((os.getcwd()), 'temp')  # string for file path to Temp folder
        if not os.path.exists("temp"):
            os.mkdir("temp")
            print("Directory created")
        print('Files will be saved in ', self.temp_pdfs)

        self.source = urllib.request.urlopen('https://www.national-lottery.co.uk/games/gamestore/scratchcards').read()
        self.soup = bs.BeautifulSoup(self.source, 'lxml')
        self.table = self.soup.table

        self.table_rows = self.table.find_all('tr')  # table_rows list, not standard list type. BS4 element result set.
        self.sc_list = []

    def scrape(self):
        for tr in self.table_rows[1:]:  # for tableresults in tablerows. Skip first item.
            td = tr.find_all('td')  # tabledata in tablerow
            row = [i.text for i in td]  # row = make list of text in table row (BSlist, not normal)

            """IMAGE & PDF """
            # image_pdf = tr.find_all("a", href=True)
            for a in tr.find_all('a'):
                # print(a['href'])
                row.append(str(a['href']))  # image & pdf

            """ add temp folder"""
            row.append(self.temp_pdfs)

            """ STORE DATA """
            self.sc_list.append(Scratchcards(row))  # list of objects
            # print("Row data: " + str(row))

        # print(self.sc_list[0])
        # print(self.sc_list[1])
        # print(self.sc_list[2])
        # print(self.sc_list[3])

    def verify(self):
        for index, scratchcard in enumerate(self.sc_list):
            if not self.sc_list[index].check_data():
                #print("Something wrong with:")
                print(self.sc_list[index])

            #print(index, scratchcard)



scrape = Scraper()
scrape.scrape()
scrape.verify()
