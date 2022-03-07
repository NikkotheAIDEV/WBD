from query import Connection

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

query = "SELECT * FROM Passenger LIMIT 3"
records = connection.query(query)
print("rows = " + str(len(records)) + "\n")
for row in records:
    print("ID = ", row[0])
    print("Name = "+ str(row[1])+ "\n")

connection.stopConnection()