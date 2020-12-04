import bs4 as bs  # webscraper
import urllib.request
import logging
from datetime import datetime
import tempfile
from sc_mysql import SC_Mysql
from scratchcards import Scratchcards
from sc_status import SC_Status


class Scraper:
    def __init__(self):

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

    def get_status(self):
        status = SC_Status()
        status.connect()
        dict_of_alive_rt, dead_list = status.get_remainingtops()
        status.disconnect()
        return dict_of_alive_rt, dead_list

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
            """ 1: gamename 2: gamenumber 5: remainingtop """

            print("gamenumber: " + str(type(row[2])) + str(row[2]))
            self.sc_list.append(Scratchcards(row))  # list of objects

            # print("Row data: " + str(row))
    def dead_or_nochange(self):
        dict_of_alive_rt, dead_list = self.get_status()
        """
        IF VALID IS FALSE. DELETE. 
        IF DEAD DELETE. 
        IF RT == THEN DELETE"""

    """ Check and Completes data, PDF scraping """
    def verify(self):
        for index, scratchcard in enumerate(self.sc_list):
            self.sc_list[index].check_data()
            if not self.sc_list[index].valid:   # if data is invalid
                self.log("Deleting Scratchcard from processing because something invalid:\n" + str(self.sc_list[index]))
                del self.sc_list[index]         # delete item from list
                # TODO: ADD LOG
    """ store in DB"""
    def store(self):
        for index, scratchcard in enumerate(self.sc_list):
            sc_db = SC_Mysql(self.sc_list[index])   # create instances
            sc_db.process()

            """ Moving the dead """
            sc_db.create_dead()
            sc_db.move_dead()

            # upload to db

s = Scraper()
s.scrape()