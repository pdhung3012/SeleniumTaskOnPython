fopRoot='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/papers/'
fpLogDownloadOld=fopRoot+'logDownload_v2.txt'
fpLogDownload=fopRoot+'logDownload.txt'
fpLogStatusPaper=fopRoot+'logStatusPaper.txt'

f1=open(fpLogDownloadOld,'r')
arrAll=f1.read().strip().split('\n')
f1.close()
lstAfter=[]
for i in range(0,len(arrAll)):
    arrItemTab=arrAll[i].split('\t')
    if(len(arrItemTab)>=4):
        if not(arrItemTab[2].startswith('https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=') and arrItemTab[3].startswith('ERROR: ')) :
            lstAfter.append(arrAll[i])

f1=open(fpLogDownload,'w')
f1.write('\n'.join(lstAfter))
f1.close()
