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
def getDomain(strLink):
    strResult=''
    arrUrl=strLink.split('/')
    if( len(arrUrl)>=4):
        strResult='/'.join(arrUrl[0:3]).replace('http://','').replace('https://','').strip()
    return strResult

def download_by_wget(pdf_url,fpPdfLocation):
    # paper_title = get_paper_title(paper_id)
    # save_title = paper_title.replace(' ', '_')
    # Get pdf url by paper id. Refer to
    #   http://stackoverflow.com/questions/22800284/download-papers-from-ieee-xplore-with-wget
    # pdf_url = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={}'.format(paper_id)
    # print(pdf_url)
    fopPdf=os.path.dirname(fpPdfLocation)+'/'
    namePdf=os.path.basename(fpPdfLocation)
    sp.call('wget "{}" -O {}'.format(pdf_url,fpPdfLocation), shell=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)


def getPdfContent(driver,strDomain, urlLink,fopTempData,indexView,fpPdfLocation):
    strResult = 'ERROR: NOT SUPPORTED'
    strRedirectLink=urlLink
    try:

        if strDomain=='ieeexplore.ieee.org':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink=urlLink.replace('/document/','/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber=')
            # isPDFValid = False
            # countReset=0
            # while(not isPDFValid):
            #     import PyPDF2
            #     f1=None
            #     try:
            #         sp.call('wget "{}" -O {}'.format(strRedirectLink, fpPdfLocation), shell=True, stderr=sp.DEVNULL,
            #                 stdout=sp.DEVNULL)
            #         time.sleep(timeWaitInSecond)
            #         f1=open(fpPdfLocation, "rb")
            #         pdf = PyPDF2.PdfFileReader(f1)
            #         if not f1 is None:
            #             f1.close()
            #         # isPDFValid=True
            #     except:
            #         print("invalid PDF file {}\n{}\t{}".format(fpPdfLocation,isPDFValid,strRedirectLink))
            #         if not f1 is None:
            #             f1.close()
            #     else:
            #         isPDFValid=True
            #         # print("Valid PDF!")
            #         # print(pdf.getDocumentInfo())
            #     if not isPDFValid:
            #         try:
            #             print('refresh')
            #             sp.call('sudo bash {}'.format(fpBashInternet), shell=True)
            #             countReset=countReset+1
            #             if countReset%5==0:
            #                 time.sleep(300)
            #             else:
            #                 time.sleep(timeWaitInSecond)
            #         except:
            #             pass
            # strResult='Success downloaded the file!'


            driver.get(urlLink)
            btnPdf=driver.find_element(By.XPATH,'//a[contains(@class,"pdf-btn-link") and contains(@class,"stats-document-lh-action-downloadPdf_2 pdf")]')
            btnPdf.click()
            time.sleep(timeWaitInSecond)
            strResult = 'Success downloaded the file!'

        elif  strDomain=='dl.acm.org':
            strResult = 'ERROR: NOT SUPPORTED'
            strRedirectLink = urlLink.replace('/doi/', '/doi/pdf/')
            # sp.call('wget "{}" -O {}'.format(strRedirectLink, fpPdfLocation), shell=True, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
            # strResult = 'Success downloaded the file!'
            createDirIfNotExist(fopTemp)
            driver.get(strRedirectLink)
            maxCount = 20
            indexCount = 0
            while (len(glob.glob(fopTemp + '*.pdf')) == 0 and indexCount <= maxCount):
                time.sleep(timeWaitInSecond)
                indexCount = indexCount + 1
            list_of_files = glob.glob(fopTemp + '*.pdf')  # * means all if need specific format then *.csv
            latest_file_pdf = max(list_of_files, key=os.path.getctime)

            shutil.copyfile(latest_file_pdf, fpPdfLocation)
            shutil.rmtree(fopTemp)
            createDirIfNotExist(fopTemp)
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
                                              "//font[contains(text(),'pdf-format:')]/../following-sibling::td//a[@itemprop='url']")
            strRedirectLink=aLink.get_attribute('href')
            print(strRedirectLink)
            # input('aaaaa')
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
fpBashInternet=fopSearchDomain+'runResetInternet.sh'
fopTemp=fopSearchDomain+'temp/'
createDirIfNotExist(fopSearchDomain)
createDirIfNotExist(fopTemp)
createDirIfNotExist(fopPaperLocation)
timeWaitInSecond=3

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

# profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
#                "download.default_directory": fopTemp , "download.extensions_to_open": "applications/pdf"}
# options.add_experimental_option("prefs", profile)
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

lstSpecificDomains=['ieeexplore.ieee.org']

for i in range(0,maxSize):
    try:
        for j in range(0, len(lstSpecificDomains)):
            try:
                keyDomain=lstSpecificDomains[j]
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
                    input('aaa ')
                    # if (indexView % 30 == 0):
                    #     print('sleep in 30 seconds')
                    #     time.sleep(30)

            except:
                traceback.print_exc()
        # if i==2:
        #     break
    except:
        traceback.print_exc()






