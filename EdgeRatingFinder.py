from selenium import webdriver

from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ratingBot:

    def __init__ (self):
        
        self.driver= webdriver.Edge(executable_path='C:\\Users\\Work\\webdrivers\\msedgedriver.exe')
        teacher='Jason Yalim'       
        self.driver.get('https://www.ratemyprofessors.com')
        sleep(4)
        self.driver.find_element_by_xpath('/html/body/div[10]/button[2]').click()
        print("here")
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="searchr"]').send_keys(teacher)

mybot=ratingBot()