from selenium import webdriver
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


class classBot:

    def __init__(self, myClassSubject, myClassNumber):

        # lines 11-18 open the catalog and list of all options of the class you selected
        self.driver = webdriver.Chrome('C:\\Users\\Work\\webdrivers\\chromedriver.exe')
        self.Subject = myClassSubject
        self.Number = myClassNumber
        self.driver.get("https://webapp4.asu.edu/catalog/")
        sleep(1.5)
        self.driver.find_element_by_xpath('//*[@id="subjectEntry"]').send_keys(self.Subject)
        self.driver.find_element_by_xpath('//*[@id="catNbr"]').send_keys(self.Number)
        self.driver.find_element_by_xpath('//*[@id="go_and_search"]').click()
        sleep(2)

        # 23: gets the url of the searched class page
        myUrl = self.driver.page_source
        # 25-27: downloads the web page and stores it

        # html parsing
        page_soup = soup(myUrl, "html.parser")

        NumClasses = page_soup.findAll('div', {"style": "vertical-align: top; font-size: smaller"})
        NumbClassesStr = str(NumClasses)
        numLine = NumbClassesStr.split('\n')
        for x in numLine:
            st = x.strip()
            break
        st = st[len(st) - 3:len(st)]
        NumClassesInt = int(st.strip())

        # finding initial teacher
        containers = page_soup.findAll('tr', {"id": "informal"})
        # adding the rest of the teachers
        x = 0
        informalNum = 0
        for x in range(0, NumClassesInt):
            informalNumber = 'informal_' + str(informalNum)
            containers += page_soup.findAll('tr', {"id": informalNumber})
            x += 1
            informalNum += 1

        # creating a str list of the teachers 'tr' files
        results = []
        for teachers in containers:
            results.append(str(teachers))

        # Adding names to a list by calling getfirstline and getProfName to just get their names
        profNameList = []
        for x in results:
            firstline = self.getfirstline(x)
            ProfName = self.getProfName(firstline)
            if ProfName != ' ':
                profNameList.append(ProfName)

        # printing list of all teacher names
        print(profNameList)

        # saving to excel document
        file = open('teacherlist.csv', 'w', newline='')

        with file:
            header = ['Teacher Name', 'Rating']
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writeheader()
            x = 0
            for items in profNameList:
                currentRating= self.getProfRating(profNameList[x])
                writer.writerow({'Teacher Name': profNameList[x]})
                writer.writerow({'Rating':currentRating})
                x += 1

    # First Line Splitter
    def getfirstline(self, result):
        lubes = result.split('\n')
        for x in lubes:
            st = x.strip()
            break
        return st

    # first name getter
    def getProfName(self, line):
        count = 0
        firstdash = 0
        lastdash = 50
        location = 0
        # finding the location of the name, will use this to get the substring of the name.
        for x in line:
            if x == '-':
                count += 1
            if count == 3:
                firstdash = location
            if count == 5:
                lastdash = location
            location += 1
            if location == lastdash:
                break
        # getting substring of the name and returning it
        name = line[firstdash + 2:lastdash + 1]
        name = name.replace('-', ' ')
        return name

    def getProfRating(self, prof):
        tRating= self.ratingBot(prof)
        print(tRating)
        return tRating

    def ratingBot(self,prof):
        # ignoring ssl verifications through chrome webdriver options
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument('acceptInsecureCerts')
        options.add_argument('--ignore-certificate-errors')

        #opening webdriver and going to ratemyprofessor website
        self.driver = webdriver.Chrome('C:\\Users\\Work\\webdrivers\\chromedriver.exe', options=options)
        self.driver.get('http://www.ratemyprofessors.com')

        #finding the professor by exiting the initial warning message and searching the teachers name.
        teacher= prof

        #MUST FIND WAY TO SPECIFY TO GET THE CORRECT PROFESSOR


        self.driver.find_element_by_xpath('/html/body/div[10]/button[2]').click()
        self.driver.find_element_by_xpath('//*[@id="searchr"]').send_keys(teacher)
        self.driver.find_element_by_xpath('//*[@id="searchr"]').send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li/a').click()
        myUrl = self.driver.page_source
        # html parsing
        page_soup = soup(myUrl, "html.parser")
        ovr = page_soup.findAll('div', {'class': 'RatingValue__Numerator-qw8sqy-2 liyUjw'})
        ovrString= str(ovr)
        ovrString=ovrString[len(ovrString)-10:len(ovrString)-7]
        self.driver.close()
        return ovrString


    # entering class subject and number for the computer to run the program for:
myClassSubject = 'MAT'
myClassNumber = '343'
myBot = classBot(myClassSubject, myClassNumber)
