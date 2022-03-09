# Have to get id and most liked category + interested in categories, then find suatable museums(6 based on favourite + rating sorted in 5.0->0.0, 4 based on interested_in + rating > 2.0)

from cgi import test
from query import Connection
import numpy as np

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

# Get the data from the person table
query_person = "SELECT * FROM Person"
records_person = connection.query(query_person)
data_person = np.array(records_person)

# Create a dictionary containing the favourite category
most_liked_dic = {"1": "1"}
for x in range(1000):
    person_id = data_person[x, 0]
    category_id = data_person[x, 3]
    most_liked_dic[person_id] = category_id

# Accessing items
# print(most_liked_dic["6"])

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
        if person_id == data_interested_in[y, 1]:

            # Check for a repeat
            if data_interested_in[y, 2] not in all_entries:
                all_entries.append(data_interested_in[y, 2])

        # Save into the dictionary
        interested_in_dic[person_id] = all_entries

connection.stopConnection()