from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os
import time
import glob
import pandas as pd
from datetime import datetime
from PdfMinerHandler import *
import urllib.request
import shutil
import pdfkit
import subprocess as sp
import spacy
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        lstPages=PDFPage.create_pages(doc)
        index=0
        for page in lstPages:
            index=index+1
            interpreter.process_page(page)

    return index, output_string.getvalue()

def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")


fopRoot='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers/'
fopOutOKPdf='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers_ok/'
fopOutFailedPdf='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers_failed/'
fopOutTextPdf='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers_text/'

createDirIfNotExist(fopOutTextPdf)

lstFopPdfInput=sorted(glob.glob(fopRoot+'**/'))
for fopSub in lstFopPdfInput:
    lstFpPdfInput=sorted(glob.glob(fopSub+'/*.pdf'))
    for i in range(0,len(lstFpPdfInput)):
        nameOfPdf=os.path.basename(lstFpPdfInput[i]).replace('.pdf','')
        print('prepare {} {}'.format(i,  lstFpPdfInput[i]))
        try:
            intValue=int(nameOfPdf)
            divValue=intValue//1000+1
            fopOutputPdfOK=fopOutOKPdf+str(divValue)+'/'
            fopOutputPdfFailed = fopOutFailedPdf + str(divValue) + '/'
            fopOutputText = fopOutTextPdf+str(divValue)+'/'
            createDirIfNotExist(fopOutputPdfFailed)
            createDirIfNotExist(fopOutputPdfOK)
            createDirIfNotExist(fopOutputText)
            num_pages,strContent=convert_pdf_to_string(lstFpPdfInput[i])
            f1=open(fopOutputText+nameOfPdf+'.tzt','w')
            f1.write('{}\n\n\n{}'.format(num_pages,strContent))
            f1.close()
            if os.path.getsize(lstFpPdfInput[i])<=10000000:
                shutil.move(lstFpPdfInput[i],fopOutputPdfOK+nameOfPdf+'.pdf')
                print('{}/{} success {}'.format(i,len(lstFpPdfInput),lstFpPdfInput[i]))
            else:
                print('{}/{} failed (larrge than 10MB {} {}'.format(i, len(lstFpPdfInput), nameOfPdf, lstFpPdfInput[i]))
                shutil.move(lstFpPdfInput[i], fopOutputPdfFailed + nameOfPdf + '.pdf')
        except:
            print('{}/{} failed {} {}'.format(i,len(lstFpPdfInput),nameOfPdf,lstFpPdfInput[i]))
            shutil.move(lstFpPdfInput[i], fopOutputPdfFailed + nameOfPdf + '.pdf')
            traceback.print_exc()
            pass
    # break
    # if len(lstFpPdfInput)>0:
    #     break






