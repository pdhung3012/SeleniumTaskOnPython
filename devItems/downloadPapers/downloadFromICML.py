from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import os
import time

def createDirIfNotExist(fopOutput):
    try:
        # Create target Directory
        os.makedirs(fopOutput, exist_ok=True)
        #print("Directory ", fopOutput, " Created ")
    except FileExistsError:
        print("Directory ", fopOutput, " already exists")

fpChromeDriver='/Users/hungphan/git/COMS-319-TA/Fall-2021/HW4-UITest/chromedriver'
fopUrl='logConferences/'
lstYears=[2021,2020,2019]
strConferenceName='icml'
createDirIfNotExist(fopUrl)
driver = webdriver.Chrome(executable_path=fpChromeDriver)
for year in lstYears:
    strHtmlName = '{}/{}{}.html'.format(strConferenceName, strConferenceName, year)
    strUrlName = 'url_{}_{}.txt'.format(strConferenceName, year)
    driver.get("https://dblp.org/db/conf/" + strHtmlName)

    elements=driver.find_elements(By.XPATH,"//li[contains(@class, 'entry') and contains(@class, 'proceedings')]")
    lstStrs=[]
    for i in range(0,len(elements)):
        try:
            ele=elements[i]
            # print(ele.text)
            eleTitle=ele.find_element(By.XPATH,".//cite/span[@class='title' and @itemprop='name']" )
            strTitle=eleTitle.text.replace('\r\n',' ').replace('\n',' ').replace('\t',' ').strip()
            eleAuthor = ele.find_element(By.XPATH, ".//cite/span[@itemprop='author']")
            strAuthor = eleAuthor.text.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
            eleLink = ele.find_element(By.XPATH, ".//nav[@class='publ']/ul/li/div[@class='head']/a")
            strLink = eleLink.get_attribute('href').replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
            strLine='{}\t{}\t{}\t{}'.format(i,strTitle,strAuthor,strLink)
            lstStrs.append(strLine)
            # print('{}\t{}'.format(i,strTitle))
        except:
            traceback.print_exc()
    f1=open(fopUrl+strUrlName,'w')
    f1.write('\n'.join(lstStrs))
    f1.close()
    time.sleep(0.2)
driver.close()
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
