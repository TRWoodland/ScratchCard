import bs4 as bs  # webscraper
import urllib.request
import logging
from datetime import datetime
import tempfile
from sc_mysql import SC_Mysql
from scratchcards import Scratchcards


class Scraper:
    def __init__(self):
        """ LOGGER """
        # self.logger = logging.getLogger('Scraper')  # create logger with 'name'
        # self.logger.setLevel(logging.DEBUG)
        # self.fh = logging.FileHandler(datetime.today().strftime("Logfile %d %B %Y.log"))  # create file handler which logs even debug messages
        # self.fh.setLevel(logging.DEBUG)
        # # self.ch = logging.StreamHandler()  # create console handler with a higher log level
        # # self.ch.setLevel(logging.ERROR)
        # # create formatter and add it to the handlers
        # self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # self.fh.setFormatter(self.formatter)
        # # self.ch.setFormatter(self.formatter)
        # # # add the handlers to the logger
        # self.logger.addHandler(self.fh)
        # # self.logger.addHandler(self.ch)
        if len(logging.getLogger().handlers) > 0:
            # The Lambda environment pre-configures a handler logging to stderr. If a handler is already configured,
            # `.basicConfig` does not execute. Thus we set the level directly.
            logging.getLogger().setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)


        """ TEMPDIR """
        self.temp_pdfs = tempfile.gettempdir()  # string for file path to Temp folder
        print('Files will be saved in ', self.temp_pdfs)

        """ INIT THE SOUP"""
        self.source = urllib.request.urlopen('https://www.national-lottery.co.uk/games/gamestore/scratchcards').read()
        self.soup = bs.BeautifulSoup(self.source, 'lxml')
        self.table = self.soup.table

        self.table_rows = self.table.find_all('tr')  # table_rows list, not standard list type. BS4 element result set.
        self.sc_list = []

    @staticmethod
    def log(cls, string):
        logging.error(string)
        print(string)

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
            sc_db = SC_Mysql(self.sc_list[index])   # create instances
            sc_db.process()
            # upload to db

