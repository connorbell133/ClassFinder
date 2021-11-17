from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ratingBot:

    def __init__(self):
        # ignoring ssl verifications through chrome webdriver options
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors-spki-list")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument('acceptInsecureCerts')
        options.add_argument('--ignore-certificate-errors')

        #opening webdriver and going to ratemyprofessor website
        self.driver = webdriver.Chrome('C:\\Users\\Work\\webdrivers\\chromedriver.exe', options=options)
        self.driver.get('http://www.ratemyprofessors.com')
        sleep(.2)

        #finding the professor by exiting the initial warning message and searching the teachers name.
        teacher= "Bruno Welfert"
        self.driver.find_element_by_xpath('/html/body/div[10]/button[2]').click()
        self.driver.find_element_by_xpath('//*[@id="searchr"]').send_keys(teacher)
        self.driver.find_element_by_xpath('//*[@id="searchr"]').send_keys(Keys.ENTER)
        sleep(2)

        self.driver.find_element_by_xpath('/html/body/div[3]/div[4]/div/div/div[2]/ul/li/a').click()

        myUrl = self.driver.page_source
        # html parsing
        page_soup = soup(myUrl, "html.parser")
        ovr = page_soup.findAll('div', {'class': 'RatingValue__Numerator-qw8sqy-2 liyUjw'})
        ovrString= str(ovr)
        ovrString=ovrString[len(ovrString)-10:len(ovrString)-7]
        print("Class= MAT 343")
        print("Teacher Name= "+ "Bruno Welfert")
        print("teacher rating = "+ovrString)

mybot = ratingBot()
