import sys
import os
sys.path.append("..")

import time
import json

import urllib.request
import urllib.parse

from tqdm import tqdm
from bs4 import BeautifulSoup
from os import path
from config import Config
from util import Util

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ExploitDBScrapper:
    BASE_URL = 'https://www.exploit-db.com'
    TABLE_ID = 'exploits-table'
    TR_TAG = 'tr'
    TD_TAG = 'td'
    VERIFIED_CLASS = 'mdi mdi-check mdi-18px'
    CODE_CLASS = 'code[class*=language]'
    MAX_ENTRIES = 120
    XPATH_DROPDOWN = "//select[@name='exploits-table_length']/option[text()='120']"
    XPATH_NEXT_BUTTON = '//a[text()="Next"]'

    def __init__(self, num_pages, timeout):
        self.documents = Util.load_json()
        self.num_pages = num_pages
        self.timeout = timeout

    def scrape(self):
        """Creates a selenium driver and scrapes Eploit DB
        """
        driver = webdriver.Chrome()
        driver.get(self.BASE_URL)
        
        self.scrape_table_page(driver)
        # self.scrape_exploit_code()
        driver.close()
    
    def scrape_table_page(self, driver):
        """Scrapes table by pages
        
        Args:
            driver (webdriver): browser used for scraping
        """
        
        driver.find_element_by_xpath(self.XPATH_DROPDOWN).click()
        num_pages_scrapped = (len(self.documents)/self.MAX_ENTRIES) - 1

        for curr_page in tqdm(range(self.num_pages)):
            time.sleep(self.timeout)

            if curr_page > num_pages_scrapped:
                self.scrape_table(driver)
                self.save_json()

            driver.find_element(By.XPATH, self.XPATH_NEXT_BUTTON).click()
            
    def scrape_table(self, driver):
        """Scraps table columns and rows
        
        Args:
            driver (webdriver): browser used for scraping
        """
        table = driver.find_element(By.ID, self.TABLE_ID)
        rows = table.find_elements(By.TAG_NAME, self.TR_TAG)
        for i, row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, self.TD_TAG)

            if len(cols) != 8:
                continue

            content_url = cols[4].find_element(
                By.TAG_NAME, 'a').get_attribute("href")

            if content_url not in self.documents:
                self.documents[content_url] = self.create_document(cols)

    def open_page(self, url):
        """Given a url it makes a request to get the html content
        and initialize an instance of beutifulsoup
        
        Args:
            url (str): url to be parsed
        
        Returns:
            BeautifulSoup: html parser
        """
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, features="html.parser")
        return soup

    def scrape_exploit_code(self):
        """Scrapes the code of the eploits using beutiful soup
        """
        for rel_url, document in self.documents.items():
            url = urllib.parse.urljoin(self.BASE_URL, rel_url)
            bs = self.open_page(url)
            document['code'] = bs.select_one(self.CODE_CLASS).text
            time.sleep(self.timeout)

    def create_document(self, cols):
        """Scrapes data from columns and stores it in a dictionary
        
        Args:
            cols (list): columns of a row in the exploit table
        
        Returns:
            dict: document dictionary
        """
        document = dict()
        document['timestamp'] = cols[0].text
        document['verified'] = 'verified' if self.is_verified(
            cols[3]) else 'not verified'
        document['title'] = cols[4].text
        document['exploit_type'] = cols[5].text
        document['plataform'] = cols[6].text
        document['author'] = cols[7].text

        return document

    def is_verified(self, td):
        """Checks the icon in the column to determine
        if the exploit is verified or not
        
        Args:
            td (Column): verified column
        
        Returns:
            bool: true if verfied false otherwise
        """
        try:
            td.find_element(By.CLASS_NAME, self.VERIFIED_CLASS)
            return True
        except:
            return False

    def save_json(self):
        """Saves exploits in a josn file
        """
        with open(Config.PATH_EXPLOITS, 'w') as exploit_file:
            json.dump(self.documents, exploit_file)
