from src.query import Connection
from src.utillities import Utillities

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

# Test utillities
utils = Utillities()
results = utils.search("Aeronautics", 100, 0)
print(results)

# Close the connection
connection.stopConnection()