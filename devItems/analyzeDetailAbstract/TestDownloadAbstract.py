from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os
import time
import glob
import pandas as pd
from datetime import datetime
import codecs
import urllib.request
import pdftotextsimple
from PdfMinerHandler import *

def getAbstractContent(driver, urlLink,fopTempData):
    strResult = 'ERROR: NOT SUPPORTED'
    try:

        arrContent=urlLink.split('/')
        strDomain='/'.join(arrContent[:3])
        if strDomain=='https://ieeexplore.ieee.org':
            # # mobile-toggle-btn
            strResult = 'ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            driver.get(strCurrentLink)
            try:
                btnShowMore = driver.find_element(By.XPATH, "//a[contains(@class, 'abstract-text-view-all')]")
                if (not btnShowMore is None) and btnShowMore.text=='(Show More)':
                    # input('aaaa')
                    btnShowMore.click()
            except:
                pass
            # abstract-mobile-div
            # hide-desktop
            divAbstract = driver.find_element(By.XPATH,
                                              "//div[contains(@class, 'abstract-text') and contains(@class, 'row')]")
            strResult=str(divAbstract.text).replace('\n',' ').replace('\t',' ')
        elif  strDomain=='https://dl.acm.org':
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH, "//div[contains(@class, 'hlFld-Abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'https://aclanthology.org':
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH, "//div[contains(@class, 'card-body') and contains(@class, 'acl-abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'https://openreview.net':
            strResult='ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            driver.get(strCurrentLink)
            # / following - sibling::span
            # and contains(text(), 'Abstract :')
            arrSpans = driver.find_elements(By.XPATH,
                                              "//strong[contains(@class, 'note-content-field')]")
            for spanItem in arrSpans:
                strText=spanItem.text.strip()
                if strText.startswith('Abstract'):
                    divAbstract=spanItem.find_element(By.XPATH,
                                              ".//following-sibling::span")
                    strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
                    break
        elif strDomain=='https://drops.dagstuhl.de':
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH, "//h3[contains(text(), 'Abstract')]/..")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'http://proceedings.mlr.press':
            strResult='ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH, "//div[(@id= 'abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'https://proceedings.neurips.cc' or strDomain == 'https://papers.nips.cc':
            strResult='ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH, "//h4[contains(text(), 'Abstract')]/following-sibling::p/following-sibling::p")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'https://www.statmt.org':
            strResult='ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            # strBibLink=strCurrentLink.replace('pdf','bib')
            # print(strBibLink)
            response = urllib.request.urlopen(strCurrentLink)
            fpTempPdf = fopTempData + 'temp.pdf'
            fpTempText = fopTempData + 'temp.txt'
            file = open(fpTempPdf, 'wb')
            file.write(response.read())
            file.close()

            strTextPaper=convert_pdf_to_string(fpTempPdf)
            f1 = open(fpTempText, 'w')
            f1.write(strTextPaper)
            f1.close()
            strAbstract=strTextPaper.split('\nAbstract\n')[1].split('\nIntroduction\n')[0].replace('\n',' ')
            startIndex=-1
            endIndex=-1
            arrPaperLines=strTextPaper.split('\n')
            for i in range(0,len(arrPaperLines)):
                if arrPaperLines[i].strip()=='Abstract':
                    startIndex=i
                elif arrPaperLines[i].strip()=='Introduction':
                    endIndex=i
                    break


            if startIndex>=0 and endIndex>=0:
                strAbstract='\n'.join(arrPaperLines[startIndex+1:endIndex]).strip()
                strResult = str(strAbstract).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'https://ojs.aaai.org':
            strResult='ERROR: NOT SUPPORTED'
            time.sleep(0.5)
            driver.get(strCurrentLink)
            divAbstract = driver.find_element(By.XPATH,
                                              "//section[contains(@class, 'item') and contains(@class, 'abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
    except Exception as e:
        strResult='ERROR: '+str(e).replace('\n',' ').replace('\t',' ')
        traceback.print_exc()
    return strResult


def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")



fpChromeDriver='/Users/hungphan/git/COMS-319-TA/Fall-2021/HW4-UITest/chromedriver'
fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fopSearchDomain=fopRoot+'searchOutputOfDomains/'
fpDetail=fopSearchDomain+'details.txt'
fopTextOutput=fopSearchDomain+'abstracts/'
fopTemp=fopSearchDomain+'temp/'
createDirIfNotExist(fopTextOutput)
createDirIfNotExist(fopTemp)
fpTextAbstract=fopTextOutput+'absContent.txt'
driver = webdriver.Chrome(executable_path=fpChromeDriver)

f1=open(fpDetail,'r')
arrUrls=f1.read().strip().split('\n')
f1.close()

if not os.path.isfile(fpTextAbstract):
    f1=open(fpTextAbstract,'w')
    f1.write('')
    f1.close()

setOfSuccessLink=[]
f1=open(fpTextAbstract,'r')
arrAbstractDownloaded=f1.read().strip().split('\n')
for i in range(0,len(arrAbstractDownloaded)):
    arrTabs=arrAbstractDownloaded[i].split('\t')
    if(len(arrTabs)>=2):
        if not arrTabs[1].startswith('ERROR: '):
            setOfSuccessLink.append(arrTabs[0])

setOfSuccessLink=set(setOfSuccessLink)

for i in range(0,len(arrUrls)):
    try:
        arrItemsInLine=arrUrls[i].split('\t')
        strCurrentLink=arrItemsInLine[1]
        if strCurrentLink in setOfSuccessLink:
            print('already download {}'.format(strCurrentLink))
            continue
        print('prepare {}'.format(strCurrentLink))
        strResult=getAbstractContent(driver,strCurrentLink,fopTemp)
        strContent='{}\t{}'.format(strCurrentLink,strResult)
        f1 = open(fpTextAbstract, 'a')
        f1.write(strContent+'\n')
        f1.close()

    except:
        traceback.print_exc()

driver.close()