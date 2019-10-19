
import time
import json

from bs4 import BeautifulSoup
from os import path
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException        

class ExploitDBScrapper:
    BASE_URL = 'https://www.exploit-db.com'
    TABLE_ID = 'exploits-table'
    TR_TAG = 'tr'
    TD_TAG = 'td'
    VERIFIED_CLASS =  'mdi mdi-check mdi-18px'
    
    def __init__(self, num_pages, timeout):
        self.documents = self.load_documents()
        self.num_pages = num_pages
        self.timeout = timeout
        
    def load_documents(self):
        if path.exists("exploit.json"):
            with open('exploit.json') as json_file:
                return json.load(json_file)
        else:
            return dict()
            
    def scrape(self):
        driver = webdriver.Chrome()
        driver.get(self.BASE_URL)
        # driver.find_element_by_xpath("//select[@name='exploits-table_length']/option[text()='120']").click()
        self.scrape_table(driver)
        driver.close()
        self.scrape_exploit_code()
        self.save_csv()
    
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

    def scrape_table(self, driver):
        time.sleep(self.timeout)
        for _ in range(self.num_pages):
            table = driver.find_element(By.ID, self.TABLE_ID)
            rows = table.find_elements(By.TAG_NAME, self.TR_TAG)
            for i, row in enumerate(rows):       
                cols = row.find_elements(By.TAG_NAME, self.TD_TAG) #note: index start from 0, 1 is col 2
                if len(cols) != 8:
                    continue
                
                content_url = cols[4].find_element(By.TAG_NAME, 'a').get_attribute("href")
                if content_url not in self.documents:
                    self.documents[content_url] = self.create_document(cols)
                    
            driver.find_element(By.XPATH, '//a[text()="Next"]').click()
            time.sleep(self.timeout)
            
    def scrape_exploit_code(self):
        for rel_url, document in self.documents.items():
            url = urllib.parse.urljoin(self.BASE_URL, rel_url)
            print(url)
            bs = self.open_page(url)
            document['code'] = bs.select_one('code[class*=language]').text
            time.sleep(self.timeout) 
            
        
    def create_document(self, cols):
       
        timestamp = cols[0].text
        verified = 'verified' if self.is_verified(cols[3]) else 'not verified'
        title = cols[4].text
        exploit_type = cols[5].text
        plataform = cols[6].text
        author = cols[7].text
        
        return {"timestamp":timestamp, "vefiied":verified, "title":title, "exploit_type":exploit_type, "platafom":plataform, "author":author}
    
    def is_verified(self, td):
        try:
            td.find_element(By.CLASS_NAME, self.VERIFIED_CLASS) 
            return True
        except:
            return False
        
    def save_csv(self):
        with open('exploit.json', 'w') as exploit_file:
            json.dump(self.documents, exploit_file)
            
