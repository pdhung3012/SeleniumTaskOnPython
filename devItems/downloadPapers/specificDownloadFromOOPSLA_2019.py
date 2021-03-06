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
strConferenceName='oopsla'
createDirIfNotExist(fopUrl)
driver = webdriver.Chrome(executable_path=fpChromeDriver)
strUrlName = 'url_{}_{}.txt'.format(strConferenceName, 2019)
driver.get("https://conf.researchr.org/track/splash-2019/splash-2019-oopsla#event-overview")

divSection = driver.find_elements(By.XPATH, "//div[ @id='event-overview']/table")
lstStrs = []
# print('len {}\n{}'.format(len(ulElements),ulElements[2].text))
try:
    for j in range(0, len(divSection)):
        # print(ulItem.text)
        ulItem = divSection[j]
        strSession = 'UnknownSession'

        elements = ulItem.find_elements(By.XPATH,
                                        ".//tr/td[2]")
        for i in range(0, len(elements)):
            try:
                ele = elements[i]
                # print(ele.text)
                eleTitle = ele.find_element(By.XPATH, ".//a")
                strTitle = eleTitle.text
                strTitle = strTitle.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                eleAuthor = ele.find_element(By.XPATH, ".//div[@class='performers']")
                strAuthor = eleAuthor.text.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                eleLink=ele.find_element(By.XPATH, ".//a[@class='publication-link navigate' and contains(text(), ' DOI') ]")
                strLink = eleLink.get_attribute('href').replace('\r\n', ' ').replace('\n', ' ').replace('\t',
                                                                                                        ' ').strip()
                strLine = '{}\t{}\t{}\t{}\t{}'.format(i + 1, strSession, strTitle, strAuthor, strLink)
                lstStrs.append(strLine)
                print(strLine)
                # print('{}\t{}'.format(i,strTitle))
            except:
                traceback.print_exc()
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
