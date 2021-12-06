from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os
import glob
import time

def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")

fopRoot='../../../../media/dataPapersExternal/collectPapers/'
fpChromeDriver=fopRoot+'chromedriver/chromedriver'
fopUrl=fopRoot+'urlConferences/'
fopDownloadPaper=fopRoot+'downloads/'
fopLogDownloadPaper=fopRoot+'downloads_log/'
createDirIfNotExist(fopDownloadPaper)
createDirIfNotExist(fopLogDownloadPaper)
lstYears=[2021,2020,2019]
strConferenceName='fse'
lstUrls=sorted(glob.glob(fopUrl+'url_'+strConferenceName+'_*.txt'),reverse=True)
# createDirIfNotExist(fopUrl)
for fileUrl in lstUrls:
    f1=open(fileUrl,'r')
    arrUrls=f1.read().strip().split('\n')
    f1.close()
    arrFileItems=fileUrl.split('/')
    urlName=arrFileItems[len(arrFileItems)-1]
    confAndYear=arrFileItems[len(arrFileItems)-1].replace('url_','').replace('.txt','')
    fopDownloadDir=fopDownloadPaper+str(confAndYear)+'/'
    createDirIfNotExist(fopDownloadDir)
    options = webdriver.ChromeOptions()
    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
               "download.default_directory": fopDownloadDir, "download.extensions_to_open": "applications/pdf"}
    options.add_experimental_option("prefs", profile)
    driver = webdriver.Chrome(executable_path=fpChromeDriver, chrome_options=options)
    f1=open(fopLogDownloadPaper+urlName,'w')
    f1.write('')
    f1.close()
    for link in arrUrls:
        arrItemInLink=link.split('/')
        isLinkOK=False
        indexDownload=0
        # https: // dl.acm.org / doi / pdf / 10.1145 / 3468264.3473487
        pdfLink='https://dl.acm.org/doi/pdf/'+arrItemInLink[len(arrItemInLink)-2]+'/'+arrItemInLink[len(arrItemInLink)-1]
        while(indexDownload<=3 or not isLinkOK):
            try:
                time.sleep(0.2)
                driver.get(pdfLink)
                isLinkOK=True
            except:
                isLinkOK=False
                traceback.print_exc()
            indexDownload=indexDownload+1
        f1 = open(fopLogDownloadPaper + urlName, 'a')
        strMessage='{}\t{}\n'.format(link,isLinkOK)
        print(strMessage)
        f1.write(strMessage)
        f1.close()
        break
    driver.close()
