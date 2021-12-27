from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os
import time
import glob
import pandas as pd
from datetime import datetime


def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")
fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fopOutputSearch=fopRoot+'searchOutputOfPapers/'

eventid = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
fopInput=fopRoot+'logConferences_ML/'
fonSearchName='Parallel-In-ML'
lstKeyWords=[('parallel',1)]

fopSearchResultFolder=fopOutputSearch+fonSearchName+'/'
import shutil
if os.path.exists(fopSearchResultFolder) and os.path.isdir(fopSearchResultFolder):
    shutil.rmtree(fopSearchResultFolder)
createDirIfNotExist(fopSearchResultFolder)

lstFpUrlFiles=sorted(glob.glob(fopInput+'*.txt'),reverse=True)
fpCsvSearchSpace=fopSearchResultFolder+'inputSearch.csv'
fpExcelSearchSpace=fopSearchResultFolder+'inputSearch.xlsx'
fpOutputCsvSearchResult=fopSearchResultFolder+'result_'+fonSearchName+'.csv'
fpOutputExcelSearchResult=fopSearchResultFolder+'result_'+fonSearchName+'.xlsx'
fpOutputLogMessage=fopSearchResultFolder+'logMessage.txt'

lstTotalInput=['Num\t"Conference"\tYear\t"Track"\t"Title"\t"Author"\t"Link"']
lstTotalOutput=['Num\tScoreMatch\t"HitWords"\t"Conference"\tYear\t"Track"\t"Title"\t"Author"\t"Link"']
index=0
for i in range(0,len(lstFpUrlFiles)):
    fpUrlItem=lstFpUrlFiles[i]
    fileName=os.path.basename(fpUrlItem).replace('.txt','')
    conf=fileName.split('_')[1]
    year=int(fileName.split('_')[2])
    print(fpUrlItem)
    try:
        f1=open(fpUrlItem,'r')
        arrContent=f1.read().split('\n')
        f1.close()

        for j in range(0,len(arrContent)):
            arrTabItem=arrContent[j].split('\t')
            # print('{}'.format(len(arrTabItem)))
            if len(arrTabItem)==5:
                index=index+1
                strCsvLine='\t'.join([str(index),'"'+conf+'"',str(year),'"'+arrTabItem[1]+'"','"'+arrTabItem[2]+'"','"'+arrTabItem[3]+'"','"'+arrTabItem[4]+'"'])
                lstTotalInput.append(strCsvLine)
                strTitleLower=arrTabItem[2].lower()
                scoreMatch=0
                hitWords=[]
                for k in range(0,len(lstKeyWords)):
                    itemKey=lstKeyWords[k][0]
                    if strTitleLower.count(itemKey)>0:
                        hitWords.append(itemKey)
                        scoreMatch=scoreMatch+lstKeyWords[k][1]
                if scoreMatch>0:
                    strCsvOutLine = '\t'.join(
                        [str(index),str(scoreMatch),str(hitWords), '"' + conf + '"', str(year), '"' + arrTabItem[1] + '"', '"' + arrTabItem[2] + '"',
                         '"' + arrTabItem[3] + '"', '"' + arrTabItem[4] + '"'])
                    lstTotalOutput.append(strCsvOutLine)

    except:
        traceback.print_exc()

f1=open(fpCsvSearchSpace,'w')
f1.write('\n'.join(lstTotalInput))
f1.close()

df_new = pd.read_csv(fpCsvSearchSpace, encoding='utf-8',sep='\t')
GFG = pd.ExcelWriter(fpExcelSearchSpace)
df_new.to_excel(GFG, index=False)
GFG.save()

f1=open(fpOutputCsvSearchResult,'w')
f1.write('\n'.join(lstTotalOutput))
f1.close()

df_new = pd.read_csv(fpOutputCsvSearchResult, encoding='utf-8',sep='\t')
df_new=df_new.sort_values(by=['ScoreMatch','Year'],ascending=(False,False))
df_new.to_csv(fpOutputCsvSearchResult,index=False)
GFG = pd.ExcelWriter(fpOutputExcelSearchResult)
df_new.to_excel(GFG, index=False)
GFG.save()

f1=open(fpOutputLogMessage,'w')
f1.write('{}\n{}'.format(str(lstKeyWords),fopSearchResultFolder))
f1.close()




