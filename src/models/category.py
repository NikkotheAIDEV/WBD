from models.consts import DATABASE, HOST, PASSWORD, USER
from query import Connection
class Category:
    __database_conn = None
    def __init__(self, category_name) -> None:
        self.category_name = category_name
        __database_conn = Connection(HOST, DATABASE, USER, PASSWORD)
        __database_conn.startConnection()

    def get_from_cateogry_with_limit(self, limit):
        # Create object
        pass

    def close_connection(self):
       self.__database_conn.stopConnection()
