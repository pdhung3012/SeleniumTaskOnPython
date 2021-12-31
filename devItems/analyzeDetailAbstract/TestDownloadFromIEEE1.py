import os.path

from lxml import html
import subprocess as sp
import sys
import urllib.request

def get_paper_title(paper_id):
    url = 'http://ieeexplore.ieee.org/document/{}/'.format(paper_id)
    html_content = urllib.request.urlopen(url).read()
    root = html.fromstring(html_content)
    title = root.xpath('//title/text()')[0].replace('IEEE Xplore Document - ','')
    return title

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
    # print('saved pdf to {}'.format(save_title))

def download_by_id(paper_id):
    # paper_title = get_paper_title(paper_id)
    # save_title = paper_title.replace(' ', '_')
    # Get pdf url by paper id. Refer to
    #   http://stackoverflow.com/questions/22800284/download-papers-from-ieee-xplore-with-wget
    pdf_url = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={}'.format(paper_id)
    sp.call('wget "{}" -O {}.pdf'.format(pdf_url, 'aaaa'), shell=False)
    # print('saved pdf to {}'.format(save_title))


print('abc')
try:
    # pdf_url = 'http://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&isnumber=&arnumber={}'.format('9426041')
    # pdf_url='https://dl.acm.org/doi/pdf/10.1145/3324884.3418918'
    pdf_url='https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9240634'
    fpPdfLocation='/home/hungphd/media/dataPapersExternal/collectPaperLinks/collectResults/aaa.pdf'
    download_by_wget(pdf_url,fpPdfLocation)
    # download_by_id('9426041')
except IndexError:
    print(__doc__)
    print('Usage: python {} <paper_id>'.format(__file__))

