import re
class Scratchcards:
    def __init__(self, rowdata):
        #  ['', '12 Months Richer', '1213', '£5', '£1,200,000', '4']
        self.gamename = rowdata[1]
        self.gamenumber = rowdata[2]
        self.cost = rowdata[3]
        self.bigprize = rowdata[4]
        self.remainingtop = rowdata[5]
        self.image = rowdata[6]
        self.pdf = rowdata[7]

        """ FIX IMAGE & PDF URLS """
        pattern = re.compile(r"""(page\/scratchcards\/popup\/.*\.jpg)""")
        self.image = pattern.findall(self.image)                                            # returns list
        self.image = r"""https://www.cdn-national-lottery.co.uk/c/i/""" + self.image[0]     # list to string

        pattern = re.compile(r"""(files\/scratchcards\/.*\.pdf)""")
        self.pdf = pattern.findall(self.pdf)                                                # returns list
        self.pdf = r"""https://www.national-lottery.co.uk/c/""" + self.pdf[0]               # list to string

        self.variables = [self.gamename, self.gamenumber, self.cost, self.bigprize, self.remainingtop,
                          self.image, self.pdf]                                             # for testing
        """end of init"""

    def __str__(self):
        return str("gamename: " + str(self.gamename) + "\n"
                   + "gamenumber: " + str(self.gamenumber) + "\n"
                   + "cost: " + str(self.cost) + "\n"
                   + "bigprize: " + str(self.bigprize) + "\n"
                   + "remainingtop: " + str(self.remainingtop) + "\n"
                   + "image: " + str(self.image) + "\n"
                   + "pdf: " + str(self.pdf) + "\n"
                   )

    def check_data(self):
        # if {1245, None} in {self.gamename, self.gamenumber, self.cost, self.bigprize, self.remainingtop, self.image,
        #                   self.pdf}:
        problem = ""
        """ gamename """
        if len(self.gamename) < 3:
            problem += "gamename too short\n"

        """ gamenumber """
        if len(self.gamenumber) < 4:    # TODO
            problem += "gamenumber not long enough\n"
        try:
            self.gamenumber = int(self.gamenumber)
        except ValueError:
            problem += "gamenumber not able to convert to int\n"
        except TypeError:
            problem += "gamenumber wrong data type\n"

        """ cost """
        if len(self.cost) < 1:
            problem += "cost not long enough\n"

        """ bigprize """

        """ remainingtop """

        """ image """

        """ pdf """

        print(problem)




i = r"""'https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/winterwonderlines-2020.jpg~999e'"""
p = r"""'/c/files/scratchcards/winterwonderlines-2020.pdf~3'"""

