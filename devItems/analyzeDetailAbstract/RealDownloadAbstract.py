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

def getAbstractContent(driver, urlLink,fopTempData,indexView):
    strResult = 'ERROR: NOT SUPPORTED'
    strRedirectLink=urlLink
    try:


        time.sleep(timeWaitInSecond)
        # urlLink=urlLink.replace('https://','http://')
        if not (urlLink == 'www.statmt.org' or urlLink.endswith('.pdf')):
            driver.get(urlLink)
        strRedirectLink=driver.current_url
        arrContent = strRedirectLink.split('/')
        strDomain = '/'.join(arrContent[:3]).replace('https://','').replace('http://','')
        if strDomain=='ieeexplore.ieee.org':
            # # mobile-toggle-btn
            strResult = 'ERROR: NOT SUPPORTED'
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
        elif  strDomain=='dl.acm.org':
            divAbstract = driver.find_element(By.XPATH, "//div[contains(@class, 'hlFld-Abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'aclanthology.org':
            divAbstract = driver.find_element(By.XPATH, "//div[contains(@class, 'card-body') and contains(@class, 'acl-abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'openreview.net':
            strResult='ERROR: NOT SUPPORTED'
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
        elif strDomain=='drops.dagstuhl.de':
            divAbstract = driver.find_element(By.XPATH, "//h3[contains(text(), 'Abstract')]/..")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'proceedings.mlr.press':
            strResult='ERROR: NOT SUPPORTED'
            divAbstract = driver.find_element(By.XPATH, "//div[(@id= 'abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'proceedings.neurips.cc' or strDomain == 'papers.nips.cc':
            strResult='ERROR: NOT SUPPORTED'
            divAbstract = driver.find_element(By.XPATH, "//h4[contains(text(), 'Abstract')]/following-sibling::p/following-sibling::p")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
        elif strDomain == 'www.statmt.org' or urlLink.endswith('.pdf'):
            strResult='ERROR: NOT SUPPORTED'
            # time.sleep(1)
            strRedirectLink=urlLink
            response = urllib.request.urlopen(urlLink)
            fpTempPdf = fopTempData + 'temp-{}.pdf'.format(indexView)
            fpTempText = fopTempData + 'temp-{}.txt'.format(indexView)
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
        elif strDomain == 'ojs.aaai.org':
            strResult='ERROR: NOT SUPPORTED'
            divAbstract = driver.find_element(By.XPATH,
                                              "//section[contains(@class, 'item') and contains(@class, 'abstract')]")
            strResult = str(divAbstract.text).replace('\n', ' ').replace('\t', ' ')
    except Exception as e:
        strResult='ERROR: '+str(e).replace('\n',' ').replace('\t',' ')
        traceback.print_exc()
    return strRedirectLink,strResult


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
fopLogConferences=fopRoot+'logConferences_ML/'
fpDetail=fopSearchDomain+'details.txt'
fopTextOutput=fopSearchDomain+'abstracts-full/'
fopTemp=fopSearchDomain+'temp/'
createDirIfNotExist(fopTextOutput)
createDirIfNotExist(fopTemp)
fpTextAbstract=fopTextOutput+'absContent.txt'
timeWaitInSecond=0.5
options = webdriver.ChromeOptions()
options.add_argument('--allow-insecure-localhost') # differ on driver version. can ignore.
caps = options.to_capabilities()
caps["acceptInsecureCerts"] = True
driver = webdriver.Chrome(executable_path=fpChromeDriver,desired_capabilities=caps)
lstFpUrls=sorted(glob.glob(fopLogConferences+'*.txt'),reverse=True)

# f1=open(fpDetail,'r')
# arrUrls=f1.read().strip().split('\n')
# f1.close()

if not os.path.isfile(fpTextAbstract):
    f1=open(fpTextAbstract,'w')
    f1.write('')
    f1.close()

setOfSuccessLink=[]
f1=open(fpTextAbstract,'r')
arrAbstractDownloaded=f1.read().strip().split('\n')
for i in range(0,len(arrAbstractDownloaded)):
    arrTabs=arrAbstractDownloaded[i].split('\t')
    if(len(arrTabs)>=3):
        if not arrTabs[2].startswith('ERROR: '):
            setOfSuccessLink.append(arrTabs[0])

setOfSuccessLink=set(setOfSuccessLink)

indexView=0
for id1 in range(0,len(lstFpUrls)):
    f1=open(lstFpUrls[id1],'r')
    arrUrlContents=f1.read().strip().split('\n')
    fileNameUrl=os.path.basename(lstFpUrls[id1])
    f1.close()
    for i in range(0,len(arrUrlContents)):
        try:
            arrItemsInLine=arrUrlContents[i].split('\t')
            if(len(arrItemsInLine)==5):
                strCurrentLink=arrItemsInLine[4]
                # strCurrentLink='https://doi.org/10.1609/aaai.v33i01.33015565'
                if strCurrentLink in setOfSuccessLink:
                    print('already download {}\t{}\t{}'.format(fileNameUrl,i,strCurrentLink))
                    continue
                print('prepare {}\t{}\t{}'.format(fileNameUrl,i,strCurrentLink))
                indexView = indexView + 1
                strRedirectLink,strResult=getAbstractContent(driver,strCurrentLink,fopTemp,indexView)
                strContent='{}\t{}\t{}'.format(strCurrentLink,strRedirectLink,strResult)
                print('end {}\t{}\t{}\t{}\t{}'.format(indexView,fileNameUrl, i, strCurrentLink,strResult[0:20]))
                f1 = open(fpTextAbstract, 'a')
                f1.write(strContent+'\n')
                f1.close()

                if (indexView % 10 == 0):
                    print('sleep in 2 seconds')
                    time.sleep(2)

        except:
            traceback.print_exc()



driver.close()