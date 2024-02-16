from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import time
import re

#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException

'''
Handle for the browser instance.
Functions include:
- loading a website from a URL
- closing the browser
'''
class Browser:

    def __init__(self):

        browser_options = Options()
        browser_options.headless = True

        # this doesn't work properly in chrome, try Firefox
        browser_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=browser_options)

    '''
    Loads the website and parses it.
    Args: None
    Return: WebElement pointing to the body of webpage
            str        unique_id which is part of the URL
    '''
    def load_website(self, url: str) -> WebElement:
        self.driver.get(url)

        # search for the body of the HTML page and return it
        body = self.driver.find_element(By.TAG_NAME, "body")
        unique_id = self._extract_unique_id(url)

        return body, unique_id

    def close(self) -> None:
        self.driver.quit()
    
    def wait(self):
        #planning_tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]")))
        time.sleep(3)

    '''
    Takes the URL and extracts the unique ID from it.
    '''
    def _extract_unique_id(self, url: str) -> str:
        unique_id = re.findall("i[0-9]{5}", url)[0]
        return unique_id       