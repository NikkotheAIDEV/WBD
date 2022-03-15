from src.query import Connection

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Terziev123'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

class Utillities:
    def search(self, name, limit = 100, offset = 0) -> list:
        
        search_query = "SELECT * FROM Museums WHERE museum_name LIKE '%{}%' LIMIT {} OFFSET {}".format(name, limit, offset)
        results = connection.query(search_query)
        return results