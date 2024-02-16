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
                print (index, row)
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

        print (hotel_data)

        with open(self.csv_file_name, 'w', newline='') as file:

            writer = csv.writer(file)
            writer.writerow(self.hotel_names)
            writer.writerow(self.hotel_urls)

            #total_size = len(hotel_data[0])


                








if __name__ == "__main__":

    table = Table("../TMB_huts.csv")

    print(table.get_hotel_url_data())