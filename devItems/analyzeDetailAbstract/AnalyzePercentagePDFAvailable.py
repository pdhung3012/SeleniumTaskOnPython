fopRoot='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers/'
fpLogDownload=fopRoot+'logDownload.txt'
fpLogStatusPaper=fopRoot+'logStatusPaper.txt'

def getDomain(strLink):
    strResult=''
    arrUrl=strLink.split('/')
    if( len(arrUrl)>=4):
        strResult='/'.join(arrUrl[0:3]).replace('http://','').replace('https://','').strip()
    return strResult


f1=open(fpLogDownload,'r')
arrAll=f1.read().strip().split('\n')
f1.close()
dictLinkAndId={}
for i in range(0,len(arrAll)):
    arrItemTab=arrAll[i].split('\t')
    if(len(arrItemTab)>=4):
        if arrItemTab[3].startswith('ERROR: '):
            if arrItemTab[2] not in dictLinkAndId.keys():
                dictLinkAndId[arrItemTab[2]]=[arrItemTab[0],0]
        else:
            if arrItemTab[2] not in dictLinkAndId.keys():
                dictLinkAndId[arrItemTab[2]]=[arrItemTab[0],1]
            else:
                dictLinkAndId[arrItemTab[2]][1] = 1

numDownloadable=0
lstInfoToFiles=[]
dictStatistics={}
for key in dictLinkAndId.keys():
    val=dictLinkAndId[key]
    strDomain=getDomain(key)
    if val[1]==1:
        numDownloadable=numDownloadable+1
    if strDomain not in dictStatistics.keys():
        dictStatistics[strDomain]=[val[1],1]
    else:
        dictStatistics[strDomain] =[dictStatistics[strDomain][0]+ val[1],dictStatistics[strDomain][1]+ 1]

per=numDownloadable*1.0/len(dictLinkAndId.keys())
print('percentage download {}/{}={}'.format(numDownloadable,len(dictLinkAndId.keys()),per))
for strDomain in dictStatistics.keys():
    lstVal=dictStatistics[strDomain]
    perItem=lstVal[0]*1.0/lstVal[1]
    print('domain {} {}/{}={}'.format(strDomain,lstVal[0], (lstVal[1]), perItem))

