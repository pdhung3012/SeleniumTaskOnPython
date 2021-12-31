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
nlp = spacy.load('en_core_web_sm')

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)

fopRoot='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers/'
fpLogDownloadOnlyIEEE=fopRoot+'logDownload_onlyIEEE.txt'
fopPdf='/home/hungphd/media/dataPapersExternal/collectPaperLinks/paperIEEE/'
fopOutPdf='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers/IEEE/'
fpFirefoxDriver='/home/hungphd/softwares/firefoxdriver/geckodriver'
timeWaitInSecond=0.5


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#object of Options class
op = Options()
#save file to path defined for recent download with value 2
op.set_preference("browser.download.folderList",2)
#disable display Download Manager window with false value
op.set_preference("browser.download.manager.showWhenStarting", False)

#MIME set to save file to disk without asking file type to used to open file
op.set_preference
("browser.helperApps.neverAsk.saveToDisk",
"application/octet-stream,application/pdf")

op.set_preference
("plugin.scan.plid.all",
False)
op.set_preference
("plugin.scan.Acrobat",
"99.0")

op.set_preference('pdfjs.disabled',True)
#set geckodriver.exe path
driver = webdriver.Firefox(executable_path=fpFirefoxDriver,
options=op)

f1=open(fpLogDownloadOnlyIEEE,'r')
arrAll=f1.read().strip().split('\n')
f1.close()
lstAfter=[]

lstFpPdf=glob.glob(fopPdf+'*.pdf')
lstNameAndText=[]
for item in lstFpPdf:
    name=os.path.basename(item)
    text=name.replace('.pdf','').replace('_',' ').lower()
    lstNameAndText.append([name,text])

for i in range(0,len(arrAll)):
    arrItemTab=arrAll[i].split('\t')
    if i<=50:
        continue
    if(len(arrItemTab)>=4):
        try:
            driver.get(arrItemTab[1])
            time.sleep(timeWaitInSecond)
            h1Tag=driver.find_element(By.XPATH,'//h1[@class="document-title"]')
            strText=h1Tag.text
            fileName=strText.replace(' ','_').replace(':','').replace(' - ','__')+'.pdf'
            fpItem=fopPdf+fileName
            if os.path.isfile(fpItem):
                fpOutput=fopOutPdf+arrItemTab[0]+'.pdf'
                if(not os.path.exists(fpOutput)):
                    shutil.copy(fpItem,fpOutput)
                    print('{} success {} {}'.format(i,arrItemTab[0],fpOutput))
                else:
                    print('{} already {} {}'.format(i, arrItemTab[0], fpOutput))
            else:
                lstScore=[]
                for item in lstNameAndText:
                    # print('aaa {}\nbbb {}'.format(strText,item[1]))
                    score=jaccard_similarity(strText.lower().split(),item[1].split())
                    lstScore.append(score)
                max_val=max(lstScore)
                idx=lstScore.index(max_val)
                item=lstNameAndText[idx]
                print('{} need manually retrieve {} {} {}'.format(i,arrItemTab[0],strText,arrItemTab[1]))
                print('alternative {} {}'.format(max_val,item[0]))
                # key=input('press key (N/n to reject the alter)')
                # if not (key.lower()=='n'):
                fpOutput = fopOutPdf + arrItemTab[0] + '.pdf'
                fpAlterItem=fopPdf+item[0]
                shutil.copy(fpAlterItem, fpOutput)
                print('{} success {} {}'.format(i, arrItemTab[0], fpOutput))
        except:
            print('{} {} {} error'.format(i, arrItemTab[0], arrItemTab[1]))
            traceback.print_exc()
            input('press key')
            pass


driver.close()