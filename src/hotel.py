from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from collections import namedtuple

from datetime import datetime
import time
import logging

HotelData = namedtuple("HotelData", "date spots")
HotelInfo = namedtuple("HotelInfo", "name url")

class HotelParser:

    END_SEASON_DATE = datetime(2024, 9, 1)

    WAIT_TIME = 3

    DAYS_TABLE_XPATH  = "/html/body/div[1]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/table/tbody/tr[2]"
    TABLE_TAG_NAME    = "td"

    DATE_CLASS_NAME       = "entete"
    PLACES_AVL_CLASS_NAME = "places"

    NEXT_WEEK_CLASS_NAME = "os_sem_suiv"

    '''
    time_date of the format: "13 FÉVR. MAR."
    '''
    @staticmethod
    def _sanitize_time(time_date: str) -> None:

        YEAR = 2024
        french_to_months = {"FÉVR.": 2, "MARS": 3, "AVRIL": 4, "MAI" : 5, "JUIN": 6, "JUIL.": 7, "AOÛT": 8, "SEPT.": 9, "OCT.": 10}

        time_date = time_date.split(' ')
        month = french_to_months[time_date[1]]
        date  = int(time_date[0])

        return datetime(YEAR, month, date)

    def __init__(self, body: WebElement, unique_id: str, date_from: datetime, date_to: datetime):

        self.PLANNING_TABLE_ID = "planning" + unique_id[1:]

        _start_time = time.time()

        if date_to > HotelParser.END_SEASON_DATE:
            raise Exception("End date has exceeded the season date.")

        self.data = []
        self.website_body = body

        can_start = lambda from_date, data: from_date in [datum.date for datum in data if datum.date == from_date]
        can_stop  = lambda to_date, data: to_date in [datum.date for datum in data if datum.date == to_date]

        _start = False

        while (True):

            data_this_week = self._get_data_for_this_week()

            # Start searching until we find the start date
            if not can_start(date_from, data_this_week) and not _start:
                logging.warning("Skipping week...")
                self._go_to_next_week()
                continue
            else:
                _start = True

            # Stop searching if we exceed the end date
            if can_stop(date_to, data_this_week):
                break

            self.data = self.data + data_this_week
            self._go_to_next_week()
        
        _end_time = time.time()

        logging.warning("Parsing took %d seconds", _end_time - _start_time)

    def _get_data_for_this_week(self) -> list:

        logging.warning("Fetching another week...")

        data = []

        # Navigate to the availability table
        planning_tab = self.website_body.find_element(By.ID, self.PLANNING_TABLE_ID)
        days_table = planning_tab.find_element(By.XPATH, HotelParser.DAYS_TABLE_XPATH)
        days_list  = days_table.find_elements(By.TAG_NAME, HotelParser.TABLE_TAG_NAME)

        # The first and last ones are for arrow and not days, so exclude them
        days_list = days_list[1:8]

        for day in days_list:
            date  = day.find_element(By.CLASS_NAME, HotelParser.DATE_CLASS_NAME).text.split("\n")
            full_date = date[1] + ' ' + date[0]
            
            date      = HotelParser._sanitize_time(full_date)
            spots_avl = day.find_element(By.CLASS_NAME, HotelParser.PLACES_AVL_CLASS_NAME)

            spots = spots_avl.text

            if not spots.isalnum():
                spots = 0

            data.append(HotelData(date, spots))

        return data
    
    def _go_to_next_week(self) -> None:

        # Point to the "Next week" button
        # TODO Below two lines could be redundant!
        planning_tab = self.website_body.find_element(By.ID, self.PLANNING_TABLE_ID)
        next_week = planning_tab.find_element(By.CLASS_NAME, HotelParser.NEXT_WEEK_CLASS_NAME)

        # Click the "Next week" button
        next_week.click()
        time.sleep(HotelParser.WAIT_TIME)
    
    '''
    Get the data after parsing the hotels availability table
    Args: None
    Return: list of (date, available spots)
    '''
    def get_data(self) -> list:
        return self.data

