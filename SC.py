import bs4 as bs  # webscraper
import urllib.request
import requests  # downloads files
import re  # regex
import pprint as pp  # prettyprint
import os  # for finding current working directory
from scratchcards import Scratchcards
from Logger import SC_Logfile
import logging
from datetime import datetime
from sc_mysql import SC_Mysql

class Scraper:
    def __init__(self):
        """ LOGGER """
        self.logger = logging.getLogger('Scraper')  # create logger with 'name'
        self.logger.setLevel(logging.DEBUG)
        self.fh = logging.FileHandler(datetime.today().strftime("Logfile %d %B %Y.log"))  # create file handler which logs even debug messages
        self.fh.setLevel(logging.DEBUG)
        self.ch = logging.StreamHandler()  # create console handler with a higher log level
        self.ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)
        # # add the handlers to the logger
        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

        """ TEMPDIR """
        self.temp_pdfs = os.path.join((os.getcwd()), 'temp')  # string for file path to Temp folder
        if not os.path.exists("temp"):
            os.mkdir("temp")
            print("Directory created")
        print('Files will be saved in ', self.temp_pdfs)

        """ INIT THE SOUP"""
        self.source = urllib.request.urlopen('https://www.national-lottery.co.uk/games/gamestore/scratchcards').read()
        self.soup = bs.BeautifulSoup(self.source, 'lxml')
        self.table = self.soup.table

        self.table_rows = self.table.find_all('tr')  # table_rows list, not standard list type. BS4 element result set.
        self.sc_list = []

    def log(self, string):
        self.logger.error(string)
        print(string)

    def scrape(self):
        self.logger.info("Process starting")
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
            #self.logger.info('creating an instance')
            self.sc_list.append(Scratchcards(row))  # list of objects
            # print("Row data: " + str(row))

        # print(self.sc_list[0])
        # print(self.sc_list[1])
        # print(self.sc_list[2])
        # print(self.sc_list[3])

    """ Check and Completes data, PDF scraping """
    def verify(self):
        for index, scratchcard in enumerate(self.sc_list):
            self.sc_list[index].check_data()
            if not self.sc_list[index].valid:   # if data is invalid
                self.log("Deleting Scratchcard from processing because something invalid:\n" + str(self.sc_list[index]))
                del self.sc_list[index]         # delete item from list

    """ store in DB"""
    def store(self):
        for index, scratchcard in enumerate(self.sc_list):
            sc_db = SC_Mysql(self.sc_list[index])
            sc_db.process()


scrape = Scraper()
scrape.scrape()
scrape.verify()
scrape.store()
