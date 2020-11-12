import fitz
def pdf_to_text():
    f = r"""temp/2mpurple.pdf"""
    text = ''
    with fitz.open(f) as doc:
        for page in doc:
            text += page.getText()
    print(text)
pdf_to_text()