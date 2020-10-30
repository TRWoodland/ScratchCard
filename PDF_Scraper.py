from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re


class PDF_Scraper:
    def __init__(self, tempdir):
        self.tempdir =  tempdir

    def pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)  # had to remove codec=codec to get it to work
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    #### Regex Probability ###################

    SCprobSearch = []  # make list
    SCprobResults = []  # make list
    SCTotalAtLaunchSearch = []
    SCTotalAtLaunchResults = []

    for i in range(len(SCpdf)):
        print('Extracting probabilities from:', SCpdf[i])

        SCprobSearch = ''  # this is where search is stored.
        pdfFile = os.path.join(tempPdfs, SCpdf[i])  # file and location

        pdfText = pdf_to_txt(pdfFile)  # Uses pdf_to_txtdef. Copies pdf text to pdfText.
        SCprobRegex = re.compile(r'\d* in \d*\.\d*')  # build search for ## in ##.##
        SCprobSearch = SCprobRegex.search(pdfText)  # Save search of pdfText in SCprobSearch.group()
        SCprobResults.append(SCprobSearch.group())  # copies the 'match item' result into a list

        ############# For total cards at launch ##############
        pdfText.replace('\n', '    ')
        SCTotalAtLaunchRegex = re.compile('....................Prizes are won, the number',
                                          re.DOTALL)  # search works for normal ones
        # and for +/- ones
        xx = re.search('''(\W\w\d*,\d*,\d*\W\w\W\w).*As Prizes are won, the number''', pdfText, re.DOTALL)

        SCTotalAtLaunchSearch = SCTotalAtLaunchRegex.search(pdfText)  # Save search of pdfText
    #    SCTotalAtLaunchResults.append(SCTotalAtLaunchSearch.group()) #copies the 'match item' result into a list

    # regex for finding total number of cards sold at launch if no line breaks (\d*\W*\d*\W*\d*)\\['n']\\(nAs Prizes are won,)
    # regex for finding total number of cards sold at launch if on multiline (\W\d*\S\d*\S\d*)\Wn\W\W\W\W\\n\W\W\W\WAs Prizes are won
