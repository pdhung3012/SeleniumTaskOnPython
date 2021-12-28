fopRoot='/Users/hungphan/git/dataPapers/collectPaperLinks/'
fopAbstractFull=fopRoot+'searchOutputOfDomains/abstracts-full/'
fpInput1=fopAbstractFull+'absContent-SE.txt'
fpInput2=fopAbstractFull+'absContent-ML.txt'
fpAll=fopAbstractFull+'absCombine.txt'

f1=open(fpInput1,'r')
arr1=f1.read().strip().split('\n')
f1.close()
f1=open(fpInput2,'r')
arr2=f1.read().strip().split('\n')
f1.close()

strCombine='{}\n{}'.format('\n'.join(arr1),'\n'.join(arr2))
f1=open(fpAll,'w')
f1.write(strCombine)
f1.close()
