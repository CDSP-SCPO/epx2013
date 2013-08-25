#BEGIN pyPdf

import pyPdf

def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = pyPdf.PdfFileReader(file(path, "rb"))
    # Extract text from page and add to content
    content += pdf.getPage(0).extractText()
    # Collapse whitespace
    #~ content = " ".join(content.replace("\xa0", " ").strip().split())
    return content
    
    

#~ date=getPDFContent("st07027.en00.pdf")
#~ date=getPDFContent("st12741-ad01re01.en00.pdf")
#~ date=getPDFContent("st15984.en09.pdf")
#~ begin=date.index('Brussels')
#~ date=date[begin+10:]
#~ print date

#END pyPdf

#BEGIN pdfminer first try

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def extractTextFromPdf(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str

doc="st07027.en00.pdf"
doc="st08397.en00.pdf"
doc="st12741-ad01re01.en00.pdf"
doc="st13107.en99.pdf"
doc="st13411.en08.pdf"
doc="st15983.en09.pdf"
doc="st15984.en09.pdf"
doc="st16142.en09.pdf"

date=extractTextFromPdf(doc).strip()[:100]
#beginning of the date (line of the date)
begin=date.index('Brussels')
date=date[begin+10:]
#end of the date (end of the line, removing extra parentheses)
temp=date.split(" ")
date=temp[0]+" "+temp[1]+" "+temp[2][:4]
print date

#~ TODO
#~ 1/find function to extract first page only -> ask stackoverflow with link to the page of the function and page to go through each page
#~ 2/ change "split" by "find third occurence of"


#END pdfminer first try
