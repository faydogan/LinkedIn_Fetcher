"""
Copyright 2019 FRKN

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Prerequsites:
Python +3
Python Selenium and Chrome Driver
Python MySQL driver and MySQL server
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import mysql.connector

#Init Values
yourWindowsUsername = "#Your Username#"
chromeDriverPath = "#Chrome Driver Path#"

#LinkedIn Login Info
url = "https://www.linkedin.com/jobs/"
username = "########@gmail.com"
password = "#######"
search = "#Your Job Title"
location = "#Take Location Value From Linked Page#"

#Adding options to ChromeDriver
options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Users\\" + yourWindowsUsername + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

#Initialize Browser
browser = webdriver.Chrome(executable_path = chromeDriverPath + "\\chromedriver.exe", chrome_options=options)
browser.get(url)
browser.maximize_window()

#Wait for page to load completely
delay = 10 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ember242')))
    print("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")
	
sleep(3) #seconds

#Enter Job Serach Values and Click On Search Button
field = browser.find_element_by_xpath("//input[@id ='jobs-search-box-keyword-id-ember37']") 
field.send_keys(search)

field2 = browser.find_element_by_xpath("//input[@id ='jobs-search-box-location-id-ember37']") 
field2.send_keys(location)

button = browser.find_element_by_xpath("//div[@id='ember36']/div[1]/div[1]/button[1]") 
button.click()

#Wait For Search Results To Come
delay = 8 # seconds
try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'ember918')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

sleep(4) #seconds

#Initialize a List, Which Will Hold Job Ads Details
JobListArr = list()

fieldM = browser.find_element_by_xpath("//div[@class='pv2 ph3 flex-grow-1']/div[1]") 
size = fieldM.get_attribute("innerText")
t = int(size.split(" ")[0])

print("Found Job Ads = " + str(t))

k = 1
liT = 2
#Open All Job Postings With Order
for i in range(1,t):
	try:
		fieldM = browser.find_element_by_xpath("//h1[@class='jobs-details-top-card__job-title t-20 t-black t-normal']") 
		JobTitle = fieldM.get_attribute("innerText")
		try:
			fieldM = browser.find_element_by_xpath("//a[@class='jobs-details-top-card__company-url ember-view']") 
			firmName = fieldM.get_attribute("innerText")
		except:
			firmName = "Not In LınkedIn"
			pass

		fieldM = browser.find_element_by_xpath("//div[@id='job-details']") 
		jobdetail = fieldM.get_attribute("innerText")
		try:
			fieldM = browser.find_element_by_xpath("//div[@class='jobs-ppc-quality__content']") 
			qualificationMatch = fieldM.get_attribute("innerText")
		except:
			qualificationMatch ="N/A"
			pass

		divLocator = "//div[@class='job-card-search--two-pane  jobs-search-results__list--card--viewport-tracking-" + str(k) + " job-card-search job-card-search--column job-card-search ember-view']/artdeco-entity-lockup[1]/artdeco-entity-lockup-content[1]/h3[1]"
		
		JobListArr.append((JobTitle, firmName, jobdetail, qualificationMatch)) #Append Job Details From LinkedIn Into List
		
		#print((JobTitle, firmName, jobdetail, qualificationMatch))
		
		sleep(0.3)
		
		fieldM = browser.find_element_by_xpath(divLocator) 
		fieldM.click()
		
		k = k + 1
		
		if k == 25:
			xpathNext = "//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[" + str(liT) + "]"
			nextB = browser.find_element_by_xpath(xpathNext) 
			nextB.click()
			k = 1
			liT = liT + 1
			print("Go to the next page")
		
		print("##################################################################################################################")
		print("Done with - " + str(i) + " - " + str(JobTitle))
		print("##################################################################################################################")

		sleep(4)
	except:
		pass

#Put Results Into MySQL DB
sqlCxn = mysql.connector.connect(host="localhost", user="root", passwd="root")
sqlCursor = sqlCxn.cursor()
for x in JobListArr:
	sqlQ = r"""INSERT INTO linkedin.joblist (JobTitle, Company, JobDetails, Qualifications) VALUES (%s , %s , %s , %s )"""
	sqlV = x
	sqlCursor.execute( sqlQ, ( sqlCxn._cmysql.escape_string(x[0]), sqlCxn._cmysql.escape_string(x[1]), sqlCxn._cmysql.escape_string(x[2]), sqlCxn._cmysql.escape_string(x[3]) ) )
	sqlCxn.commit()

sqlCxn.close()