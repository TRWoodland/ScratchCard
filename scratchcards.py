import re
import requests
import os
import fitz
import logging

class Scratchcards:
    def __init__(self, rowdata):
        self.module_logger = logging.getLogger('Scraper.Scratchcards')
        #self.module_logger.info("something")
        #self.module_logger.error("thing")

        self.gamename = rowdata[1]
        self.gamenumber = rowdata[2]
        self.cost = rowdata[3]
        self.bigprize = rowdata[4]
        self.remainingtop = rowdata[5]
        self.image = rowdata[6]
        self.pdf_url = rowdata[7]
        self.temp_pdfs = rowdata[8]

        """ TEST FAULT CONDITION! """
        if self.gamename == "5X":
            # self.gamename = ""
            pass

        """ If value turns false """
        self.valid = True

        """ Information scraped later"""
        self.pdf_text = str()
        self.odds_at_launch = str()
        self.total_cards_at_launch = int()
        #self.winning_cards_launch = float()

        """ FIX IMAGE URL """
        pattern = re.compile(r"""(page\/scratchcards\/popup\/.*\.jpg)""")
        self.image = pattern.findall(self.image)                                            # returns list
        if len(self.image) == 0:                                                          # if list empty
            self.validity(str(self.gamenumber) + " RE failed to find image url: " + self.image)
        else:
            self.image = r"""https://www.cdn-national-lottery.co.uk/c/i/""" + self.image[0]     # list to string

        """ FIX PDF URL """
        pattern = re.compile(r"""(files\/scratchcards\/.*\.pdf)""")
        self.pdf_url = pattern.findall(self.pdf_url)                                        # returns list
        if len(self.pdf_url) == 0:                                                          # if list empty
            self.validity(str(self.gamenumber) + " RE failed to find PDF_URL: " + self.pdf_url)
        else:
            self.pdf_url = r"""https://www.national-lottery.co.uk/c/""" + self.pdf_url[0]       # list to string

        """ MAKE PDF FILENAME """
        self.pdf = self.pdf_url.split(r"""/""")     # split url up into list
        self.pdf = self.pdf[-1]                     # get filename

        self.variables = [self.gamename, self.gamenumber, self.cost, self.bigprize, self.remainingtop,
                          self.image, self.pdf_url]                                             # for testing
        """end of init"""

    def __str__(self):
        return str("gamename: " + str(self.gamename) + "\n"
                   + "gamenumber: " + str(self.gamenumber) + "\n"
                   + "cost: " + str(self.cost) + "\n"
                   + "bigprize: " + str(self.bigprize) + "\n"
                   + "remainingtop: " + str(self.remainingtop) + "\n"
                   + "image: " + str(self.image) + "\n"
                   + "pdf: " + str(self.pdf) + "\n"
                   + "pdf_url: " + str(self.pdf_url) + "\n"
                   + "temp_pdfs: " + str(self.temp_pdfs) + "\n"
                   + "odds_at_launch: " + str(self.odds_at_launch) + "\n"
                   + "total_cards_at_launch: " + str(self.total_cards_at_launch) + "\n"
                   #+ "winning_cards_launch: " + str(self.winning_cards_launch) + "\n"
                   )

    def validity(self, string):
        self.module_logger.error(string)
        print(string)
        self.valid = False

    def check_data(self):

        """"" gamename """""
        if not 100 > len(self.gamename) > 0:    # gamename length between 1 and 100 chars
            self.validity(str(self.gamenumber) + " gamename wrong length: " + str(self.gamename))

        """ gamenumber """
        try:
            self.gamenumber = int(self.gamenumber)
        except ValueError:
            self.validity(str(self.gamenumber) + " gamenumber not able to convert to int: " + str(self.gamenumber))
        except TypeError:
            self.validity(str(self.gamenumber) + " gamenumber wrong data type: " + str(self.gamenumber))
        if not 10000 > self.gamenumber > 999:     # game number should be 4 digits
            self.validity(str(self.gamenumber) + " gamenumber wrong length enough: " + str(self.gamenumber))

        """ cost """
        self.cost = self.cost.replace('£', '').replace(',', '')
        try:
            self.cost = float(self.cost)
        except ValueError:
            self.validity(str(self.gamenumber) + " cost not able to convert to float: " + str(self.cost))
        except TypeError:
            self.validity(str(self.gamenumber) + " cost wrong data type: " + str(self.cost))
        if self.cost < 1:
            self.validity(str(self.gamenumber) + " cost number too small: " + str(self.cost))

        """ bigprize """
        self.bigprize = self.bigprize.replace('£', '').replace(',', '')
        try:
            self.bigprize = float(self.bigprize)
            if self.bigprize < 1:
                self.validity(str(self.gamenumber) + " bigprize number too small: " + str(self.bigprize))
        except ValueError:
            self.validity(str(self.gamenumber) + " bigprize not able to convert to float: " + str(self.bigprize))
        except TypeError:
            self.validity(str(self.gamenumber) + " bigprize wrong data type: " + str(self.bigprize))

        """ remainingtop """
        try:
            self.remainingtop = int(self.remainingtop)
        except ValueError:
            self.validity(str(self.gamenumber) + " remainingtop not able to convert to int: " + str(self.remainingtop))
        except TypeError:
            self.validity(str(self.gamenumber) + " remainingtop wrong data type: " + str(self.remainingtop))

        """ image """
        # if the status code is not an error code (4xx or 5xx), it is considered ‘true’:
        if not requests.get(self.image, stream=True, timeout=3):
            self.validity(str(self.gamenumber) + " image url not working: " + str(self.image))

        """ pdf_url """
        if not isinstance(self.pdf_url, str):
            self.validity(str(self.gamenumber) + " pdf not a string: " + str(self.pdf_url))
        else:
            status = self.download_pdf()        # download file, returns status

        """ PDF """
        if not os.path.isfile(os.path.join(self.temp_pdfs, self.pdf)):
            self.validity(str(self.gamenumber) + " pdf not found: " + str(self.pdf))

        """ pdf_text """
        self.pdf_text = self.pdf_to_text()
        if not isinstance(self.pdf_text, str):
            self.validity(str(self.gamenumber) + " pdf not string: " + str(self.pdf_text))

        """ odds_at_launch and total_cards_at_launch """
        self.odds_at_launch, self.total_cards_at_launch = self.text_to_odds()

        if not self.odds_at_launch:     # if None was returned
            self.validity(str(self.gamenumber) + " odds_at_launch not found: " + str(self.odds_at_launch))

        if not self.total_cards_at_launch:     # if None was returned
            self.validity(str(self.gamenumber) + " total_cards_at_launch not found: " +
                                     str(self.total_cards_at_launch))
        else:
            self.total_cards_at_launch = self.total_cards_at_launch.replace(',', '')
            try:
                self.total_cards_at_launch = int(self.total_cards_at_launch)
                if self.total_cards_at_launch < 1000:
                    self.validity(str(self.gamenumber) + " total_cards_at_launch number too small: " +
                                             str(self.total_cards_at_launch))
            except ValueError:
                self.validity(str(self.gamenumber) + " total_cards_at_launch not able to convert to int: " +
                              str(self.total_cards_at_launch))

        """ winning cards at launch """
        # self.odds_at_launch = self.odds_at_launch.split(' in ')
        # try:
        #     self.odds_at_launch[0] = float(self.odds_at_launch[0])
        #     self.odds_at_launch[1] = float(self.odds_at_launch[1])
        #
        #     self.winning_cards_launch = self.total_cards_at_launch / self.odds_at_launch[1]  # TODO: RECALULATE
        # except ValueError:
        #     self.validity(str(self.gamenumber) + " remainingtop not able to convert to int: " +
        #                              str(self.odds_at_launch))

        """ END """

    def download_pdf(self):
        if not os.path.isfile(os.path.join(self.temp_pdfs, self.pdf)):  # if file doesn't already exist
            res_get = requests.get(self.pdf_url, stream=True, timeout=3)

            if not res_get:  # if the status code is not an error code (4xx or 5xx), it is considered ‘true’:
                self.validity(str(self.gamenumber) + " PDF download failed. Get Method Status code: " +
                                         str(res_get) + str(self.pdf_url))
                return False

            else:
                res_get = requests.get(self.pdf_url, allow_redirects=True)                    # download
                open(os.path.join(self.temp_pdfs, self.pdf), 'wb').write(res_get.content)     # save
                print("Get Method Status code ok: " + str(res_get) + " " + self.pdf_url)
                print("PDF downloaded")
                return True

        else:
            print("File already downloaded")                                            # file already exists
            return True

    def pdf_to_text(self):
        text = ''
        with fitz.open(os.path.join(self.temp_pdfs, self.pdf)) as doc:
            for page in doc:
                text += page.getText()
        return text

    def text_to_odds(self):
        re1 = r"""\d* in* \d*\.\d*"""
        odds_at_launch_re = re.compile(re1)
        odds_at_launch_re = odds_at_launch_re.search(self.pdf_text)

        re2 = r"""(?<=There are ).*\W*(?=Scratchcards)"""
        total_cards_at_launch_re = re.compile(re2)
        total_cards_at_launch_re = total_cards_at_launch_re.search(self.pdf_text)

        return odds_at_launch_re[0], total_cards_at_launch_re[0]
