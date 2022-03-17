
from models.consts import DATABASE, HOST, PASSWORD, USER
from query import Connection
class Museum(Connection):
    # __database_conn = None
    def __init__(self, name, address, country, rating, category) -> None:
        self.museum_name = name
        self.museum_address = address
        self.country = country
        self.rating = rating
        self.museum_category = category
        super().__init__(HOST, DATABASE, USER, PASSWORD)
        # __database_conn = Connection(HOST, DATABASE, USER, PASSWORD)
        # __database_conn.startConnection()

    # def insert_category(self):
    #         cursor = self.__database_conn.db_conn.cursor(prepared=True)
    #         insert_query = """INSERT INTO Categories (category_name) VALUES(%s)"""
    #         tuple1 = (self.category_name)

    #         cursor.execute(insert_query, tuple1)
    #         self.__database_conn.connection_commit()
    #         cursor.close()
    #         print("Data inserted successfully")

    # def get_from_cateogry_with_limit(self, limit):
    #     # Create object
    #     pass

    # def close_connection(self):
    #    self.__database_conn.stopConnection()

    # def search_muesum(name, limit = 100, offset = 0) -> list:
    #     results = search_museum()
    #     # search_query = "SELECT * FROM Museums WHERE museum_name LIKE '%{}%' LIMIT {} OFFSET {}".format(name, limit, offset)
    #     # results = self.connection.query(search_query)
    #     # return results

