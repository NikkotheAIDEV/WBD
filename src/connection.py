from utillities import Utillities
from query import Connection
from models import consts

# Create object
connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

# Test utillities
utils = Utillities()
results = utils.search("Nige")
print(results)

# Close the connection
connection.stopConnection()