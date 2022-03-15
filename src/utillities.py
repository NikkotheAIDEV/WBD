from src.query import Connection
from src.models import consts

# Create object
connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
connection.startConnection()

class Utillities:
    def search(self, name, limit = 100, offset = 0) -> list:
        
        search_query = "SELECT * FROM Museums WHERE museum_name LIKE '%{}%' LIMIT {} OFFSET {}".format(name, limit, offset)
        results = connection.query(search_query)
        return results