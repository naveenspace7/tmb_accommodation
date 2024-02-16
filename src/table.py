import csv
import logging

from hotel import HotelInfo

class Table:

    def __init__(self, csv_file):

        self.csv_file_name = csv_file

        self.hotel_names = []
        self.hotel_urls  = []

        self.constructed_hotels = []

        with open(self.csv_file_name, 'r') as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    self.hotel_names = row[1:]
                elif index == 1:
                    self.hotel_urls  = row[1:]

        for index in range(0, len(self.hotel_names)):
            self.constructed_hotels.append(HotelInfo(self.hotel_names[index], self.hotel_urls[index]))
    
    '''
    Return the list of all the HotelInfo constructed from the CSV file
    '''
    def get_hotel_url_data(self) -> list:
        return self.constructed_hotels
    
    def write_hotel_data(self, hotel_data) -> None:

        with open(self.csv_file_name, 'w', newline='') as file:

            writer = csv.writer(file)

            # write the headers leaving the first column empty
            writer.writerow([''] + self.hotel_names)
            writer.writerow([''] + self.hotel_urls)

            dates_len = len(hotel_data[0])

            for date_i in range(0, dates_len):

                # insert the date in the first column
                row_data = [hotel_data[0][date_i].date.date()]

                # iterate over all the hotels and add them to the rows
                for hotel in hotel_data:
                    row_data.append(hotel[date_i].spots)

                writer.writerow(row_data)
        
        logging.info("Done writing the new data.")