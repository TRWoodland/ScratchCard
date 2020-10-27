import re
class Scraper:
    def __init__(self, rowdata):
        #  ['', '12 Months Richer', '1213', '£5', '£1,200,000', '4']
        self.gamename = rowdata[1]
        self.gamenumber = rowdata[2]
        self.cost = rowdata[3]
        self.bigprize = rowdata[4]
        self.remainingtop = rowdata[5]
        self.image = rowdata[6]
        self.pdf = rowdata[7]
        print(self.image)

        """ FIX URLS """
        self.img_pattern = r"""https?://[^/\s]+/\S+\.(?:jpg|jpeg|gif|png)"""
        self.x = re.findall(self.img_pattern, self.image)
        self.image = self.x[0]
        self.imagethumbnail = self.x[1]
        self.pdf_pattern = r"""(\/c\/files).*(pdf)"""
        self.pdf = re.search(self.pdf_pattern, self.pdf)[0]

        """end of init"""

    def things(self):
        test = r"""'<a href="https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/winterwonderlines-2020.jpg~999e" target="_blank" title="This image will open in a new window"><img alt="" src="https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/thumbnails/winterwonderlines-2020-thumbnail.jpg~453d"/></a>',"""
        search = r"""https?://[^/\s]+/\S+\.(?:jpg|jpeg|gif|png)"""
