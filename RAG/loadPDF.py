from ironpdf import *
import csv
from langchain_community.document_loaders import PyPDFLoader


def loadPDF():

    renderer = ChromePdfRenderer()

    tag = input("Enter stock symbol: ")

    tag_found = False

    with open('Conference-Calls-1-14-2024.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == tag:
                url = row[3]
                pdf = renderer.RenderUrlAsPdf(url)
                name = tag + '.pdf'
                pdf.SaveAs(name)

    return name