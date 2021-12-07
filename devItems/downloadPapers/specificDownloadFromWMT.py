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
strConferenceName='wmt'
years=[21,20,19]
createDirIfNotExist(fopUrl)
driver = webdriver.Chrome(executable_path=fpChromeDriver)
for year in years:
    strUrlName = 'url_{}_20{}.txt'.format(strConferenceName, year)
    driver.get("https://www.statmt.org/wmt{}/program.html".format(year))

    divSection = driver.find_elements(By.XPATH, "//table")
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

                    if year!=19:
                        eleTitle = ele.find_element(By.XPATH, ".//a")
                        if (not eleTitle.get_attribute('href').endswith('.pdf')):
                            continue
                        strTitleRaw = eleTitle.find_element(By.XPATH,".//i").text
                        strTitle = strTitleRaw.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        # strAuthor = driver.execute_script("return arguments[0].firstChild.textContent", ele).replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        strAuthor=ele.text.replace(strTitleRaw+'\n','')
                        # print('author {}'.format(strAuthor))
                        strAuthor=strAuthor.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        strLink = eleTitle.get_attribute('href').replace('\r\n', ' ').replace('\n', ' ').replace('\t',
                                                                                                                ' ').strip()
                    else:
                        eleTitle = ele.find_element(By.XPATH, ".//i")
                        strTitleRaw = eleTitle.text
                        strTitle = strTitleRaw.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        # strAuthor = driver.execute_script("return arguments[0].firstChild.textContent", ele).replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        strAuthor = ele.text.replace(strTitleRaw + '\n', '')
                        # print('author {}'.format(strAuthor))
                        strAuthor = strAuthor.replace('\r\n', ' ').replace('\n', ' ').replace('\t', ' ').strip()
                        strLink = 'UnknownLink'

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
