
from bs4 import BeautifulSoup as bs
from requests import get
from random import shuffle, randrange


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException        

# TODO: documen :'(
# TODO add cache so if it hangs it can cntinue when it left
class ExploitDBScrapper:
    BASE_URL = 'https://www.exploit-db.com'
    TABLE_ID = 'exploits-table'
    TR_TAG = 'tr'
    TD_TAG = 'td'
    VERIFIED_CLASS =  'mdi mdi-check mdi-18px'
    
    def __init__(self, num_pages, timeout):
        self.csv = []
        self.timeout = timeout
        
    # TODO: add functionality to crawl over several pages and wait n seconds between calls (variable timeout)
    def scrap(self):
        driver = webdriver.Chrome()
        driver.get(self.BASE_URL)
        table_id = driver.find_element(By.ID, self.TABLE_ID)
        rows = table_id.find_elements(By.TAG_NAME, self.TR_TAG) # get all of the rows in the table3
        
        for i, row in enumerate(rows):       
            cols = row.find_elements(By.TAG_NAME, self.TD_TAG) #note: index start from 0, 1 is col 2
            if len(cols) != 8:
                continue

            self.csv.append(self.format_row(cols, i))
        
        driver.close()
        self.save_csv()
    
    def format_row(self, cols, i):
        timestamp = cols[0].text
        verified = 'verified' if self.is_verified(cols[3]) else 'not verified'
        title = cols[4].text
        exploit_type = cols[5].text
        plataform = cols[6].text
        author = cols[7].text
        
        return f'{i+1}, {timestamp},{verified},{title},{exploit_type},{plataform},{author}'
    
    def is_verified(self, td):
        try:
            td.find_element(By.CLASS_NAME, self.VERIFIED_CLASS) 
            return True
        except:
            return False
        
    def save_csv(self):
        with open('exploit.csv', 'w') as exploit_file:
            exploit_file.writelines(f"{row}\n" for row in self.csv)
            
