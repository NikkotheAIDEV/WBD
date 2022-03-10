# Have to get id and most liked category + interested in categories, then find suatable museums(6 based on favourite + rating sorted in 5.0->0.0, 4 based on interested_in + rating > 2.0)
from multiprocessing.dummy import Array
from query import Connection
from ast import Dict
import numpy as np
import random

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

class Helper:
    def request_person_table(self) -> Dict:
        # Get the data from the person table
        query_person = "SELECT * FROM Person"
        records_person = connection.query(query_person)
        data_person = np.array(records_person)

        # Create a dictionary containing the favourite category
        most_liked_dic = {}
        for x in range(1000):
            person_id = data_person[x, 0]
            category_id = data_person[x, 3]
            most_liked_dic[person_id] = category_id

        return most_liked_dic

    def request_interested_in_table(self) -> Dict:
        # Get the data from the interested_in table
        query_interested_in = "SELECT * FROM Interested_in"
        records_interested_in = connection.query(query_interested_in)
        data_interested_in = np.array(records_interested_in)

        # Create a dictionary containing all interested_in entries
        interested_in_dic = {}
        for x in range(2000):

            # Get the id of the person we are checking
            person_id = data_interested_in[x, 1]
            all_entries = []

            # Find every entry for this person
            for y in range(2000):
                if person_id == data_interested_in[y, 1] and data_interested_in[y, 2] not in all_entries:
                        all_entries.append(data_interested_in[y, 2])

                # Save into the dictionary
                interested_in_dic[person_id] = all_entries
        
        return interested_in_dic

    def request_fav_id(self, id) -> int:
        query_fav_id = "SELECT most_liked_category_id FROM Person WHERE id = {}".format(id)
        record_fav_id = connection.query(query_fav_id)
        return record_fav_id[0][0]

    def request_interested_in_id(self, id) -> Array:
        query_interested_in_id = "SELECT DISTINCT category_id FROM Interested_in WHERE person_id = {}".format(id)
        record_interested_in_id = connection.query(query_interested_in_id)
        if len(record_interested_in_id) != 0:
            data_interested_in_id = np.array(record_interested_in_id)
            return data_interested_in_id[0]
        return []

    # Get the 100 highest rated museums in favourite category and select 6
    def request_favourite_6(self, id) -> Array:
        query_favourites = "SELECT id FROM Museums WHERE category_id = {} ORDER BY avg_rating DESC LIMIT 100".format(id)
        records_favourite = connection.query(query_favourites)
        data_favourites = np.array(records_favourite)
        fav_arr = []

        for _ in range(6):
            z = random.randrange(1, 101)
            fav_arr.append(data_favourites[z, 0])
        
        return fav_arr

    # Get a 100 museums in interested_in category and select 4
    def request_interested_in_4(self, id = []) -> Array:

        ids = ""
        for x in range(len(id)):
            if ids == "":
                ids = ids + ("{}").format(id[x])
                print(ids)
            else:
                ids = ids + (", {}").format(id[x])
                print(ids)

        query_interested_in = "SELECT id FROM Museums WHERE category_id IN ({}) AND (avg_rating > 0.5) ORDER BY id ASC LIMIT 100".format(ids)
        print(query_interested_in)
        records_interested_in = connection.query(query_interested_in)
        data_interested_in = np.array(records_interested_in)
        interested_in_arr = []

        for _ in range(4):
            z = random.randrange(1, 101)
            interested_in_arr.append(data_interested_in[z, 0])

        return interested_in_arr

    # Documentation
    request_person_table.__doc__ = "This function returns the person table in format \{person_id\: fav_category_id\}"
    request_interested_in_table.__doc__ = "This function returns the interested_in table in format \{person_id\: [category_ids]\}"
    request_fav_id.__doc__ = "This function takes the person_id of a person and then returns there favourite category_id as an integer"
    request_interested_in_id.__doc__ = "This function takes the person_id of a person and then returns there interested_in categories ids in an array"
    request_favourite_6.__doc__ = "This function takes the category_id of a museum and then returns 6 museums from that category that have the best avg_ratings"
    request_interested_in_4.__doc__ = "This function takes an array of category_ids for museum and then returns 4 museums that might be interesting"