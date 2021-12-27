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

def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")

fpChromeDriver='/Users/hungphan/git/COMS-319-TA/Fall-2021/HW4-UITest/chromedriver'
fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fopLogConferences=fopRoot+'logConferences/'
fopOutputDomain=fopRoot+'searchOutputOfDomains/'
fpOutDo=fopOutputDomain+'domains.txt'
fpOutDe=fopOutputDomain+'details.txt'
lstFpUrls=sorted(glob.glob(fopLogConferences+'*.txt'))
topLine=1
driver = webdriver.Chrome(executable_path=fpChromeDriver)
dictLink={}
createDirIfNotExist(fopOutputDomain)
for i in range(0,len(lstFpUrls)):
    fpItemUrl=lstFpUrls[i]
    f1=open(fpItemUrl,'r')
    arrF1=f1.read().split('\n')
    f1.close()
    for j in range(0,min(len(arrF1),topLine)):
        arrTabSplit=arrF1[j].split('\t')
        if(len(arrTabSplit)>=5):
            strLink=arrTabSplit[4]
            if strLink.startswith('http') or strLink.startswith('https'):
                try:
                    time.sleep(0.5)
                    driver.get(strLink)
                    strCurrentUrl=driver.current_url
                    arrItUrls = strCurrentUrl.split('/')
                    strItDomain='/'.join(arrItUrls[:3])
                    if strItDomain not in dictLink.keys():
                        dictLink[strItDomain]=['{}\t{}'.format(strLink,strCurrentUrl)]
                    else:
                        dictLink[strItDomain].append('{}\t{}'.format(strLink, strCurrentUrl))
                except:
                    traceback.print_exc()
    # if i==2:
    #     break

f1=open(fpOutDo,'w')
f1.write('\n'.join(dictLink.keys()))
f1.close()

f1=open(fpOutDe,'w')
f1.write('')
f1.close()

for key in dictLink.keys():
    lst=dictLink[key]
    f1 = open(fpOutDe, 'a')
    f1.write('\n'.join(lst)+'\n')
    f1.close()







