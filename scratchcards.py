import re
import requests
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

class Scratchcards:
    def __init__(self, rowdata):
        #  ['', '12 Months Richer', '1213', '£5', '£1,200,000', '4']
        self.gamename = rowdata[1]
        self.gamenumber = rowdata[2]
        self.cost = rowdata[3]
        self.bigprize = rowdata[4]
        self.remainingtop = rowdata[5]
        self.image = rowdata[6]
        self.pdf_url = rowdata[7]
        self.temp_pdfs = rowdata[8]

        """ Information scraped later"""
        self.pdf_text = str()
        self.odds_at_launch = str()
        self.total_cards_at_launch = int()
        self.winning_cards_launch = float()


        """ FIX IMAGE URL """
        pattern = re.compile(r"""(page\/scratchcards\/popup\/.*\.jpg)""")
        self.image = pattern.findall(self.image)                                            # returns list
        self.image = r"""https://www.cdn-national-lottery.co.uk/c/i/""" + self.image[0]     # list to string

        """ FIX PDF URL """
        pattern = re.compile(r"""(files\/scratchcards\/.*\.pdf)""")
        self.pdf_url = pattern.findall(self.pdf_url)                                        # returns list
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
                   + "winning_cards_launch: " + str(self.winning_cards_launch) + "\n"
                   )

    def check_data(self):
        # if {1245, None} in {self.gamename, self.gamenumber, self.cost, self.bigprize, self.remainingtop, self.image,
        #                   self.pdf}:
        problem = ""
        """ gamename """
        if len(self.gamename) <= 1:
            problem += "gamename too short: " + str(self.gamename) + "\n"

        """ gamenumber """
        try:
            self.gamenumber = int(self.gamenumber)
        except ValueError:
            problem += "gamenumber not able to convert to int: " + str(self.gamenumber) + "\n"
        except TypeError:
            problem += "gamenumber wrong data type: " + str(self.gamenumber) + "\n"
        if self.gamenumber < 999:     # game number should be 4 digits
            problem += "gamenumber not long enough: " + str(self.gamenumber) + "\n"

        """ cost """
        self.cost = self.cost.replace('£','').replace(',','')
        try:
            self.cost = float(self.cost)
        except ValueError:
            problem += "cost not able to convert to float: " + str(self.cost) + "\n"
        except TypeError:
            problem += "cost wrong data type: " + str(self.cost) + "\n"
        if self.cost < 1:
            problem += "cost number too small: " + str(self.cost) + "\n"

        """ bigprize """
        self.bigprize = self.bigprize.replace('£','').replace(',','')
        try:
            self.bigprize = float(self.bigprize)
            if self.bigprize < 1:
                problem += "bigprize number too small: " + str(self.bigprize) + "\n"
        except ValueError:
            problem += "bigprize not able to convert to float: " + str(self.bigprize) + "\n"
        except TypeError:
            problem += "bigprize wrong data type: " + str(self.bigprize) + "\n"

        """ remainingtop """
        try:
            self.remainingtop = int(self.remainingtop)
        except ValueError:
            problem += "remainingtop not able to convert to int: " + str(self.remainingtop) + "\n"
        except TypeError:
            problem += "remainingtop wrong data type: " + str(self.remainingtop) + "\n"

        """ image """
        # if the status code is not an error code (4xx or 5xx), it is considered ‘true’:
        if not requests.get(self.image, stream=True, timeout=3):
            problem += "image url not working: " + str(self.image) + "\n"

        """ pdf_url """
        if not isinstance(self.pdf_url, str):
            problem += "pdf not a string: " + str(self.pdf_url) + "\n"
        else:
            status, problem = self.download_pdf(problem)        # download file, returns status

        """ PDF """
        if not os.path.isfile(os.path.join(self.temp_pdfs, self.pdf)):
            problem += "pdf not found: " + str(self.pdf) + "\n"

        """ pdf_text """
        self.pdf_text = self.pdf_to_text(os.path.join(self.temp_pdfs, self.pdf))
        if not isinstance(self.pdf_text, str):
            problem += "pdf not string: " + str(self.pdf_text) + "\n"
        #print(self.pdf_text)

        """ odds_at_launch and total_cards_at_launch """
        self.odds_at_launch, self.total_cards_at_launch = self.text_to_odds()

        if not self.odds_at_launch:     # if None was returned
            problem += "odds_at_launch not found: " + str(self.odds_at_launch) + "\n"

        if not self.total_cards_at_launch:     # if None was returned
            problem += "total_cards_at_launch not found: " + str(self.total_cards_at_launch) + "\n"
        else:
            self.total_cards_at_launch = self.total_cards_at_launch.replace(',', '')
            try:
                self.total_cards_at_launch = int(self.total_cards_at_launch)
                if self.total_cards_at_launch < 1000:
                    problem += "total_cards_at_launch number too small: " + str(self.total_cards_at_launch) + "\n"
            except ValueError:
                problem += "total_cards_at_launch not able to convert to int: " + str(self.total_cards_at_launch) + "\n"

        """ winning cards at launch """
        self.odds_at_launch = self.odds_at_launch.split(' in ')
        try:
            self.odds_at_launch[0] = float(self.odds_at_launch[0])
            self.odds_at_launch[1] = float(self.odds_at_launch[1])

            self.winning_cards_launch = self.total_cards_at_launch / self.odds_at_launch[1]  # TODO: RECALULATE
        except ValueError:
            problem += "remainingtop not able to convert to int: " + str(self.odds_at_launch) + "\n"

        """ END """
        print(problem)

    def download_pdf(self, problem):
        if not os.path.isfile(os.path.join(self.temp_pdfs, self.pdf)):  # if file doesn't already exist
            res_get = requests.get(self.pdf_url, stream=True, timeout=3)

            if not res_get:  # if the status code is not an error code (4xx or 5xx), it is considered ‘true’:
                problem += "Get Method Status code: " + str(res_get) + " " + self.pdf_url
                return False, problem

            else:
                res_get = requests.get(self.pdf_url, allow_redirects=True)                    # download
                open(os.path.join(self.temp_pdfs, self.pdf), 'wb').write(res_get.content)     # save
                print("Get Method Status code ok: " + str(res_get) + " " + self.pdf_url)
                print("PDF downloaded")
                return True, problem

        else:
            print("File already downloaded")                                            # file already exists
            return True, problem

    def pdf_to_text(self, file):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)  # had to remove codec=codec to get it to work
        with open(file, 'rb') as f:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set()
            for page in PDFPage.get_pages(f, pagenos, maxpages=maxpages, password=password, caching=caching,
                                          check_extractable=True):
                interpreter.process_page(page)
            text = retstr.getvalue()
        device.close()
        retstr.close()
        return text

    def text_to_odds(self):
        re1 = r"""\d* in* \d*\.\d*"""
        odds_at_launch_re = re.compile(re1)
        odds_at_launch_re = odds_at_launch_re.search(self.pdf_text)

        re2 = r"""(?<=There are ).*\W*(?=Scratchcards)"""
        total_cards_at_launch_re = re.compile(re2)
        total_cards_at_launch_re = total_cards_at_launch_re.search(self.pdf_text)

        return odds_at_launch_re[0], total_cards_at_launch_re[0]

i = r"""'https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/winterwonderlines-2020.jpg~999e'"""
p = r"""'/c/files/scratchcards/winterwonderlines-2020.pdf~3'"""
p2 = r"""https://www.national-lottery.co.uk/c/files/scratchcards/winterwonderlines-2020.pdf"""