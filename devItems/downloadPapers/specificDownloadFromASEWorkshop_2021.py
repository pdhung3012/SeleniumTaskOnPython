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
strConferenceName='ase'
createDirIfNotExist(fopUrl)
driver = webdriver.Chrome(executable_path=fpChromeDriver)
strUrlName = 'urlWorkshop_{}_{}.txt'.format(strConferenceName, 2021)
driver.get("file:///Users/hungphan/git/papers/paper_proceedings/ASE2021_FULL/index.html#!/toc/1")

divSection = driver.find_elements(By.XPATH, "//div[ @data-ng-repeat='section in $ctrl.conference.sections' and @class='ng-scope']")
lstStrs = []
# print('len {}\n{}'.format(len(ulElements),ulElements[2].text))
try:
    for j in range(0, len(divSection)):
        # print(ulItem.text)
        ulItem = divSection[j]
        strSession = 'UnknownSession'
        try:
            eleSessionName = ulItem.find_element(By.XPATH, ".//h3[@data-ng-class='$ctrl.getSectionClass(section)']")
            # eleSessionName=arrEleSessionName[len(arrEleSessionName)-1]
            strSession = eleSessionName.text.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
            print(strSession)
        except:
            traceback.print_exc()

        elements = ulItem.find_elements(By.XPATH,
                                        ".//div[@data-ng-repeat='item in section.lineItems']")
        for i in range(0, len(elements)):
            try:
                ele = elements[i]
                # print(ele.text)
                eleTitle = ele.find_element(By.XPATH, ".//a")
                strTitle = driver.execute_script("return arguments[0].firstChild.textContent", eleTitle)
                strTitle = strTitle.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                eleAuthor = ele.find_element(By.XPATH, ".//p")
                strAuthor = eleAuthor.text.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                strLink = eleTitle.get_attribute('href').replace('\r\n', ' ').replace('\n', ' ').replace('\t',
                                                                                                        ' ').strip()
                strLine = '{}\t{}\t{}\t{}\t{}'.format(i + 1, strSession, strTitle, strAuthor, strLink)
                lstStrs.append(strLine)
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
