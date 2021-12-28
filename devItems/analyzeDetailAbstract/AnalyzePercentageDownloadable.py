fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fopAbstractFull=fopRoot+'searchOutputOfDomains/abstracts-full/'
fpAll=fopAbstractFull+'absCombine.txt'
fpLogDownloadAbstract=fopAbstractFull+'logAbstract.txt'

f1=open(fpAll,'r')
arrAll=f1.read().strip().split('\n')
f1.close()
dictLinkAndId={}
for i in range(0,len(arrAll)):
    arrItemTab=arrAll[i].split('\t')
    if(len(arrItemTab)>=3):
        if arrItemTab[2].startswith('ERROR: '):
            if arrItemTab[1] not in dictLinkAndId.keys():
                dictLinkAndId[arrItemTab[1]]=[len(dictLinkAndId.keys())+1,0]
        else:
            if arrItemTab[1] not in dictLinkAndId.keys():
                dictLinkAndId[arrItemTab[1]]=[len(dictLinkAndId.keys())+1,1]
            else:
                dictLinkAndId[arrItemTab[1]][1] = 1

numDownloadable=0
lstInfoToFiles=[]
for key in dictLinkAndId.keys():
    val=dictLinkAndId[key]
    if val[1]==1:
        numDownloadable=numDownloadable+1
    strLine='{}\t{}\t{}'.format(key,val[0],val[1])
    lstInfoToFiles.append(strLine)

f1=open(fpLogDownloadAbstract,'w')
f1.write('\n'.join(lstInfoToFiles))
f1.close()
per=numDownloadable*1.0/len(dictLinkAndId.keys())
print('percentage download {}/{}={}'.format(numDownloadable,len(dictLinkAndId.keys()),per))

