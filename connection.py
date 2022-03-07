from query import Connection
import numpy as np
import tf

# Info
host = '127.0.0.1'
database = 'Airport'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

# Get the data
query = "SELECT * FROM Passenger LIMIT 3"
records = connection.query(query)
print(records)

# print("rows = " + str(len(records)) + "\n")
# for row in records:
#     print("ID = ", row[0])
#     print("Name = "+ str(row[1])+ "\n")

# Create a np array and transfer it to tenserflow file
arr = np.array(records)
tf.receive_data(arr)
tf.print_data()

# Close the connection
connection.stopConnection()