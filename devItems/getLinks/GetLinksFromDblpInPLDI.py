from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os

def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")

fpChromeDriver='/Users/hungphan/git/COMS-319-TA/Fall-2021/HW4-UITest/chromedriver'
fopUrl='urlConferences/'
lstYears=[2019,2020,2021]
strConferenceName='pldi'
createDirIfNotExist(fopUrl)
for year in lstYears:
    driver = webdriver.Chrome(executable_path=fpChromeDriver)
    strHtmlName='{}/{}{}.html'.format(strConferenceName,strConferenceName,year)
    strUrlName='url_{}_{}.txt'.format(strConferenceName,year)
    driver.get("https://dblp.org/db/conf/"+strHtmlName)

    elements=driver.find_elements(By.XPATH, '//a')
    # print(type(elements))
    # print(len(elements))
    lstUrls=[]
    for i in range(0,len(elements)):
        try:
            ele=elements[i]
            href=ele.get_attribute('href')
            # href.startswith('https://dl.acm.org/doi/')
            if href!= None and href!='' and href.startswith('https://doi.org/'):
                print(href)
                lstUrls.append(href)
        except:
            traceback.print_stack()

    fpUrl=fopUrl+strUrlName
    lstUrls=list(set(lstUrls))
    # lstUrls=sorted(lstUrls)
    f1=open(fpUrl,'w')
    f1.write('\n'.join(lstUrls))
    f1.close()
    driver.close()
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
