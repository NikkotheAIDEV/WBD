from models.consts import DATABASE, HOST, PASSWORD, USER
from query import Connection
import random
import numpy as np
class Museum(Connection):
    # __database_conn = None
    def __init__(self, name, address, country, rating, category, longitude, latitude, image_url) -> None:
        self.museum_name = name
        self.museum_address = address
        self.country = country
        self.rating = rating
        self.museum_category = category
        self.longitude = longitude
        self.latitude = latitude
        self.image_url = image_url
        super().__init__(HOST, DATABASE, USER, PASSWORD)

    def request_favourite(self, id, number = 6) -> list:
        query_favourites = "SELECT id FROM Museums WHERE category_id = {} ORDER BY avg_rating DESC LIMIT 100".format(id)
        records_favourite = self.query(query_favourites)
        data_favourites = np.array(records_favourite)
        fav_arr = []

        already_inserted = []
        while len(fav_arr) < number:
            z = random.randrange(1,100)
            if z not in already_inserted:
                fav_arr.append(data_favourites[z][0])
                already_inserted.append(z)

        return fav_arr

    # Get a 100 museums in interested_in category and select 4
    def request_interested(self, id = [], number = 4) -> tuple:

        ids = ""
        for x in range(len(id)):
            if ids == "":
                ids = ids + ("{}").format(id[x])
            else:
                ids = ids + (", {}").format(id[x])

        query_interested_in = "SELECT id FROM Museums WHERE category_id IN ({}) AND (avg_rating > 0.5) ORDER BY id ASC LIMIT 100".format(ids)
        records_interested_in = self.query(query_interested_in)
        data_interested_in = np.array(records_interested_in)
        interested_in = ()

        already_inserted = []
        for _ in range(number):
            while True:
                z = random.randrange(1, 100)
                if z not in already_inserted:
                    interested_in.append(data_interested_in[z, 0])
                    already_inserted.append(z)
                    break

        return interested_in