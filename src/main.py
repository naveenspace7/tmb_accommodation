from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

URL = "https://www.montourdumontblanc.com/fr/il4-refuge_i32365-auberge-du-truc.aspx"

class Browser:

    def __init__(self):

        browser_options = Options()
        browser_options.headless = True

        # this doesn't work properly in chrome, try Firefox
        browser_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=browser_options)

    def load_website(self, website) -> WebElement:
        self.driver.get(website)

        # search for the body of the HTML page and return it
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body

    def refresh(self) -> None:
        self.driver.refresh()

    def close(self) -> None:
        self.driver.quit()
    
    def wait(self):
        #planning_tab = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]")))
        time.sleep(3)

class Hotel:

    WAIT_TIME = 3

    @staticmethod
    def sanitize_time(time_in_str) -> None:


        # TODO: convert the time which in the form of string into datetime format
        pass
    
    def __init__(self, body, date_from, date_until):

        self.data = []
        self.website_body = body

    def get_data_for_this_week(self):
        
        planning_tab = self.body.find_element(By.ID, "planning32365")

        days_table = planning_tab.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]")
        days_list  = days_table.find_elements(By.TAG_NAME, "td")

        # The first and last ones are for arrow and not days
        days_list = days_list[1:8]

        for day in days_list:
            date  = day.find_element(By.CLASS_NAME, "entete").text.split("\n")
            dates = dates[1] + ' ' + dates[0]

            # TODO: Convert french into english date and time

            places = day.find_element(By.CLASS_NAME, "places")
        print (dates, places.text)
    
    def go_to_next_week(self) -> None:

        # Point to the "Next week" button
        # Below two lines could be redundant!
        planning_tab = self.body.find_element(By.ID, "planning32365")
        next_week = planning_tab.find_element(By.CLASS_NAME, "os_sem_suiv")

        next_week.click()
        time.sleep(Hotel.WAIT_TIME)

if __name__ == "__main__":

    browser = Browser()
    body = browser.load_website(URL)

    for i in range(0, 2, 1):

        data = body.find_element(By.ID, "planning32365")

        next_week = data.find_element(By.CLASS_NAME, "os_sem_suiv")
        print ("Check:", next_week.tag_name)
        table_body = data.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]")
        days = table_body.find_elements(By.TAG_NAME, "td")

        next_button = days[8]

        days = days[1:8]
        for day in days:
            dates  = day.find_element(By.CLASS_NAME, "entete").text.split("\n")
            dates = dates[1] + ' ' + dates[0]

            places = day.find_element(By.CLASS_NAME, "places")
            print (dates, places.text)
    
        next_week.click()
        
        browser.wait()

        #time.sleep(10)
    
    browser.close()