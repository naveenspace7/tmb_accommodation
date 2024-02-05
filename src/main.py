from browser import Browser
from hotel import HotelParser, HotelData, HotelInfo

from datetime import datetime

hotels = [
    HotelInfo("RefugioXYZ", "https://www.montourdumontblanc.com/fr/il4-refuge_i32365-auberge-du-truc.aspx"),
    # "",
    # "",
]

fully_parsed_data = {}

def run_checks() -> None:

    start_date = datetime(2024, 6, 1)
    end_date   = datetime(2024, 10, 1)

    if end_date > HotelParser.END_SEASON_DATE:
        raise Exception("End date has exceeded the season date - last possible date is " + HotelParser.END_SEASON_DATE.strftime("%d-%B-%Y"))

    browser = Browser()

    for hotel in hotels:

        url_body = browser.load_website(hotel.url)
        hotel = HotelParser(url_body, start_date, end_date)

        fully_parsed_data[hotel.name] = hotel.get_data()

    browser.close()


if __name__ == "__main__":

    run_checks()