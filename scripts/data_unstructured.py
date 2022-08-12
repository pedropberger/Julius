"""Let's try extract all unstructured data too
Implementantion order:
1 - download pdfs
2 - organize mongoDB
3 - OCR pdfs
4 - Elastic Search
5 - semi struture the data
6 - Portal Scraping/Crawling

---------------------------------------

https://colatina-es.portaltp.com.br/consultas/documentos.aspx?id=8
https://santamariadejetiba-es.portaltp.com.br/consultas/documentos.aspx?id=8
http://santateresa-es.portaltp.com.br/consultas/documentos.aspx?id=8

Download the pdf with the links and put it in

data\temp\colatina.pdf
data\temp\santamariadejetiba.pdf
data\temp\santateresa.pdf

"""

import tabula

file1 = "data/temp/santamariadejetiba.pdf"

table = tabula.read_pdf(file1, pages = 2)
print(table)

import PyPDF2
PDFFile = open("file.pdf",'rb')

PDF = PyPDF2.PdfFileReader(PDFFile)
pages = PDF.getNumPages()
key = '/Annots'
uri = '/URI'
ank = '/A'

for page in range(pages):
    print("Current Page: {}".format(page))
    pageSliced = PDF.getPage(page)
    pageObject = pageSliced.getObject()
    if key in pageObject.keys():
        ann = pageObject[key]
        for a in ann:
            u = a.getObject()
            if uri in u[ank].keys():
                print(u[ank][uri])
