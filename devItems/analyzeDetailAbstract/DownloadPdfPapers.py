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

def getDomain(strLink):
    strResult=''
    arrUrl=strLink.split('/')
    if( len(arrUrl)>=4):
        strResult='/'.join(arrUrl[0:3]).replace('http://','').replace('https://','').strip()
    return strResult

def getPdfContent(driver,strDomain, urlLink,fopTempData,indexView,fpPdfLocation):
    strResult = 'ERROR: NOT SUPPORTED'
    strRedirectLink=urlLink
    try:
        time.sleep(timeWaitInSecond)
        if strDomain=='ieeexplore.ieee.org':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink=urlLink.replace('/document/','/stamp/stamp.jsp?arnumber=')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            # driver.get(strRedirectLink)
            # time.sleep(timeWaitInSecond*2)
            # list_of_files = glob.glob(fopTemp + '*.pdf')  # * means all if need specific format then *.csv
            # latest_file_pdf = max(list_of_files, key=os.path.getctime)
            # shutil.copyfile(latest_file_pdf, fpPdfLocation)
            # os.remove(latest_file_pdf)
            strResult='Success downloaded the file!'
        elif  strDomain=='dl.acm.org':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink.replace('/doi/', '/doi/pdf/')
            # response = urllib.request.urlopen(strRedirectLink)
            # file = open(fpPdfLocation, 'wb')
            # file.write(response.read())
            # file.close()
            driver.get(strRedirectLink)
            maxCount=20
            indexCount=0
            while (not os.listdir(fopTemp)) and indexCount<=maxCount:
                time.sleep(timeWaitInSecond)
                indexCount=indexCount+1
            list_of_files = glob.glob(fopTemp+'*.pdf')  # * means all if need specific format then *.csv
            latest_file_pdf = max(list_of_files, key=os.path.getctime)
            shutil.copyfile(latest_file_pdf, fpPdfLocation)
            os.remove(latest_file_pdf)
            strResult = 'Success downloaded the file!'
        elif strDomain == 'aclanthology.org':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink[0:(len(urlLink)-1)]+'.pdf'
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain == 'openreview.net':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink.replace('/forum?id=', '/pdf?id=')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain=='drops.dagstuhl.de':
            strResult = 'ERROR: NOT SUPPORTED'
            driver.get(urlLink)
            aLink = driver.find_element(By.XPATH,
                                              "//a[@itemprop='url']")
            strRedirectLink=aLink.get_attribute('href')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'

        elif strDomain == 'proceedings.mlr.press':
            strResult='ERROR: NOT SUPPORTED'
            arrContent=urlLink.split('/')
            htmlName=arrContent[len(arrContent)-1].replace('.html','')
            strRedirectLink='/'.join(arrContent[0:(len(arrContent)-1)])+'/'+htmlName+'/'+htmlName+'.pdf'
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain == 'proceedings.neurips.cc' or strDomain == 'papers.nips.cc':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink.replace('/hash/', '/file/').replace('-Abstract.html', '-Paper.pdf')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain=='file://':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink.replace('/Users/hungphan/git/papers/paper_proceedings/ASE2021_FULL/', '/home/hungphd/media/dataPapersExternal/collectPaperLinks/ASE2021_FULL/')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain == 'www.statmt.org' or urlLink.endswith('.pdf'):
            strResult='ERROR: NOT SUPPORTED'
            strRedirectLink=urlLink
            response = urllib.request.urlopen(urlLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'
        elif strDomain == 'ojs.aaai.org':
            strResult = 'ERROR: NOT SUPPORTED'
            driver.get(urlLink)
            aLink = driver.find_element(By.XPATH,
                                        "//a[contains(@class, 'obj_galley_link') and contains(@class, 'pdf')]")
            strRedirectLink = aLink.get_attribute('href')
            response = urllib.request.urlopen(strRedirectLink)
            file = open(fpPdfLocation, 'wb')
            file.write(response.read())
            file.close()
            strResult = 'Success downloaded the file!'

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


# fpChromeDriver='/Users/hungphan/git/COMS-319-TA/Fall-2021/HW4-UITest/chromedriver'
# fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fpChromeDriver='/home/hungphd/softwares/chromedriver/chromedriver'
fopRoot='/home/hungphd/media/dataPapersExternal/collectPaperLinks/'
fopSearchDomain=fopRoot+'collectResults/'
fopPaperLocation=fopSearchDomain+'papers/'
fpLogAbstract=fopSearchDomain+'logAbstract.txt'
fpLogDownload=fopPaperLocation+'logDownload.txt'
fopTemp=fopSearchDomain+'temp/'
createDirIfNotExist(fopSearchDomain)
createDirIfNotExist(fopTemp)
createDirIfNotExist(fopPaperLocation)
timeWaitInSecond=0.5

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": fopTemp, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
# options.add_argument('--allow-insecure-localhost') # differ on driver version. can ignore.
# caps = options.to_capabilities()
# caps["acceptInsecureCerts"] = True
# desired_capabilities=caps
driver = webdriver.Chrome(executable_path=fpChromeDriver,options=options)


f1=open(fpLogAbstract,'r')
arrContent=f1.read().strip().split('\n')
f1.close()

if not os.path.isfile(fpLogDownload):
    f1=open(fpLogDownload,'w')
    f1.write('')
    f1.close()

setAlreadyDownloaded=[]
dictDownloadLinks={}
dictReverseDownloadLinks={}
dictListOfDomains={}

f1=open(fpLogDownload,'r')
arrDownloadedStatuses=f1.read().strip().split('\n')
f1.close()
for i in range(0,len(arrDownloadedStatuses)):
    arrLineTabs=arrDownloadedStatuses[i].split('\t')
    if len(arrLineTabs)>=4:
        if not arrLineTabs[3].startswith('ERROR: '):
            setAlreadyDownloaded.append(int(arrLineTabs[0]))
setAlreadyDownloaded=set(setAlreadyDownloaded)


for i in range(0,len(arrContent)):
    arrLineTabs=arrContent[i].split('\t')
    if len(arrLineTabs)>=3:
        dictDownloadLinks[arrLineTabs[0]]=int(arrLineTabs[1])
        dictReverseDownloadLinks[int(arrLineTabs[1])]=arrLineTabs[0]
        strDomain=getDomain(arrLineTabs[0])
        if strDomain not in dictListOfDomains.keys():
            dictListOfDomains[strDomain]=[]
        dictListOfDomains[strDomain].append(int(arrLineTabs[1]))

lstSizeOfDomain=[]
for key in dictListOfDomains.keys():
    sizeItem=len(dictListOfDomains[key])
    lstSizeOfDomain.append(sizeItem)

maxSize=max(lstSizeOfDomain)
indexView=0

for i in range(0,maxSize):
    try:
        for j in range(0, len(dictListOfDomains.keys())):
            try:
                keyDomain=list(dictListOfDomains.keys())[j]
                valListIds=dictListOfDomains[keyDomain]
                if i<len(valListIds):
                    keyId=valListIds[i]
                    urlLink=dictReverseDownloadLinks[keyId]
                    if keyId in setAlreadyDownloaded:
                        print('already download {}\t{}\t{}'.format(keyId,i, urlLink))
                        continue
                    print('prepare {}\t{}\t{}'.format(keyId, i, urlLink))
                    indexView = indexView + 1
                    nameFolderPdf=(indexView//1000)+1
                    fopPdfInside=fopPaperLocation+str(nameFolderPdf)+'/'
                    createDirIfNotExist(fopPdfInside)
                    fpPdfLocation=fopPdfInside+str(keyId)+'.pdf'
                    strRedirectLink, strResult = getPdfContent(driver,keyDomain, urlLink, fopTemp, indexView,fpPdfLocation)
                    # strRedirectLink=''
                    # strResult='ERROR: Not Supported'
                    strContent = '{}\t{}\t{}\t{}'.format(keyId,urlLink, strRedirectLink, strResult)
                    print('end {}\t{}\t{}\t{}\t{}'.format(indexView, keyDomain, i, urlLink, strResult[0:10]))
                    f1 = open(fpLogDownload, 'a')
                    f1.write(strContent + '\n')
                    f1.close()

                    if (indexView % 10 == 0):
                        print('sleep in 2 seconds')
                        time.sleep(2)

            except:
                traceback.print_exc()
        if i==10:
            break
    except:
        traceback.print_exc()






