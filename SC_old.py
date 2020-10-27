# libraries required
# pip3 install bs4, lxml, requests, re, pprint, PyPDF2, pdfminer, gspread, oauth2client

# Things to add: Error handling.
# Append date to sheet row if row is new.
#






source = urllib.request.urlopen('https://www.national-lottery.co.uk/games/gamestore/scratchcards').read()
soup = bs.BeautifulSoup(source, 'lxml')
table = soup.table

table_rows = table.find_all('tr')  # table_rows list, not standard list type. BS4 element result set.
SClist = []  # ScratchCard List of lists. All results will end up here.

for tr in table_rows:  # for tableresults in tablerows
    td = tr.find_all('td')  # td is tabledata in tablerow
    row = [i.text for i in td]  # row = make list of text in table row (BSlist, not normal)
    SClist.append(row)  # add to SClist (normal list)
    print(row)

rowCount = int(len(table_rows)) - 1  # rowCount is the number of rows, minus 1 for title

######## IMAGES #################
SCimages = []  # create list
imageCount = 0
for a in soup.find_all("a", href=True):  # find all links
    if re.findall(r".+(?=jpg|png|jpeg)", a['href']):  # if links to images
        SCimages.append(a['href'])  # Makes a List of row data
        imageCount = imageCount + 1

##### remove image address ###########
for i in range(len(SCimages)):
    SCimages[i] = SCimages[i][29:]  # removes address part
    SCimages[i] = SCimages[i][:-5]  # removes wierd bit after .jpg

######### PDF ######################
SCpdf = []  # create list
pdfcount = 0
for a in soup.find_all("a", href=True):  # find all links
    if re.findall(r".+(?=pdf)", a['href']):  # if link is pdf
        SCpdf.append(a['href'])  # append to list
        pdfcount = pdfcount + 1

#### remove /c/files/scratchcards/   and ~3 ######
for i in range(len(SCpdf)):
    SCpdf[i] = SCpdf[i][22:]  # removes address stuff
    SCpdf[i] = SCpdf[i][0:-2]  # removes ~3

##### COUNT CHECK ###############
if rowCount == imageCount == pdfcount:  # same number of datarows, pdfs and images
    print('Images, PDFs and Rows correct', imageCount, ' ', pdfcount, ' ', rowCount)
else:
    print('IMAGES PDFS AND ROWS DO NOT MATCH')

###### Manipulation ######################

del SClist[0]  # removes first item from list which is title

#### add images and pdfs to SClist
for i in range(len(SClist)):
    SClist[i][0] = SCimages[i]  # List, first position, replace with SCimage first image
    SClist[i].append(SCpdf[i])  # List, append PDF
    pp.pprint((SClist)[i])

######## download files #########

for i in range(len(SClist)):
    pdfUrl = "https://www.national-lottery.co.uk/c/files/scratchcards/" + SCpdf[i]  # location of PDF
    pdfFile = os.path.join(tempPdfs, SCpdf[i])  # builds file and location string
    if os.path.isfile(pdfFile) == False:  # does file exist? true false
        r = requests.get(pdfUrl, allow_redirects=True)
        open(pdfFile, 'wb').write(r.content)
        print(SCpdf[i], 'Downloaded')
    else:
        print(SCpdf[i], 'Already Downloaded')

####### PDF Reading using Py2PDF ###########
# Doesn't read important part.
# Left in because needs less libraries and would like to reuse code another day

pdfFile  # file string currently in memory
pdfObject = open(pdfFile, 'rb')  # open. read binary
pdfReader = PyPDF2.PdfFileReader(pdfObject)  # copy pdf contents
pdfReader.numPages  # number of pages
pageObj = pdfReader.getPage(0)  # select page
pageObj.extractText()  # extract page text. IMPORTANT TEXT MISSING.

#### alternative attempt to read PDF data using pdfminer ###########
#### from https://stackoverflow.com/questions/26494211/extracting-text-from-a-pdf-file-using-pdfminer-in-python

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


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


#### Adds probabilities to SClist #################
if len(SClist) == len(SCprobResults):  # is there the same number of probabilities to SClist items

    for i in range(len(SClist)):
        SClist[i].insert(1, (SCprobResults[i]))
else:
    print('Probabilities list doesnt have enough results')

pp.pprint(SClist)

###### Google Sheet ################
# break
print('Uploading to Google Sheets')

import gspread
import oauth2client
from oauth2client.service_account import ServiceAccountCredentials

scope = scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('PythonProjectsSecret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('PythonProjects').sheet1

SCimageAddress = '''=image("https://www.cdn-national-lottery.co.uk/c/i/page/scratchcards/popup/'''
SCimageAddressEnding = '''")'''
# sheets =image("https://images-na.ssl-images-amazon.com/images/I/61UQ6zD1KgL._SX322_BO1,204,203,200_.jpg")

GameNumberCol = []  # this will store the game numbers on the sheet
for i in range(len(SClist)):
    GameNumberColPosition = 0

    if int(SClist[i][2]) in GameNumberCol:  # is gamenumber already on board
        GameNumberColPosition = GameNumberCol.index(int(SClist[i][2]))  # find the position of the existing GN

        # for some reason a ' appears on sheets and I don't know where it came from.
        # It prevents cell imagelink working
        CellImage = (SCimageAddress + SClist[i][
            0] + SCimageAddressEnding)  # there is a bug in Sheets where is adds a ' to the begining
        # of a pasted string. remove it and the cell becomes an image.

        # BELOW. update cell, column index, first cell, image
        sheet.update_cell(GameNumberColPosition, 1, CellImage[1:])
        sheet.update_cell(GameNumberColPosition, 2, SClist[i][1])
        sheet.update_cell(GameNumberColPosition, 3, SClist[i][2])
        sheet.update_cell(GameNumberColPosition, 4, SClist[i][3])
        sheet.update_cell(GameNumberColPosition, 5, SClist[i][4])
        sheet.update_cell(GameNumberColPosition, 6, SClist[i][5])
        sheet.update_cell(GameNumberColPosition, 7, SClist[i][6])
        sheet.update_cell(GameNumberColPosition, 8, SClist[i][7])

    else:
        SClist[i][0] = (SCimageAddress + (SClist[i][0] + SCimageAddressEnding))
        sheet.append_row(SClist[i])
print('Uploaded to Google Sheet')
print('''https://docs.google.com/spreadsheets/d/16hX8VROhGu3gSfeSvsJXOXDX1KblET5ZyoUt63RLuGA/edit?usp=sharing''')

# first check if game is in

# if game is in, update row with new info

# check for first blank row


##### How long do SC run for
##### When do they start
##### Do they finish by date or by run-out of cards
#####


