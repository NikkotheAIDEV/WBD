from src.utillities import Utillities
from src.query import Connection
from src.models import consts

# Create object
connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

# Test utillities
utils = Utillities()
results = utils.search("Aeronautics", 100, 0)
print(results)

# Close the connection
connection.stopConnection()