from browser import Browser
from hotel import HotelParser, HotelData, HotelInfo

from datetime import datetime
from table import Table

def run_checks(hotels_csv: str) -> None:
    
    fully_parsed_data = []

    start_date = datetime(2024, 6, 1)
    end_date   = datetime(2024, 8, 1)

    if end_date > HotelParser.END_SEASON_DATE:
        raise Exception("End date has exceeded the season date - last possible date is " + HotelParser.END_SEASON_DATE.strftime("%d-%B-%Y"))

    browser = Browser()

    table = Table(hotels_csv)
    hotels = table.get_hotel_url_data()

    for hotel in hotels:
        url_body, unique_id = browser.load_website(hotel.url)
        hotel_parsed = HotelParser(url_body, unique_id, start_date, end_date)
        fully_parsed_data.append(hotel_parsed.get_data())

    table.write_hotel_data(fully_parsed_data)
    browser.close()


if __name__ == "__main__":

    HOTELS_TABLE = "../TMB_huts_copy.csv"

    run_checks(HOTELS_TABLE)