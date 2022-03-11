from models.consts import DATABASE, HOST, PASSWORD, USER
from query import Connection
class Museum(Connection):
    # __database_conn = None
    def __init__(self, user_id, category_id) -> None:
        self.user_id = user_id
        self.category_id = category_id
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
