import mysql.connector
from mysql.connector import Error

class Connection:
    db_conn = None
    cursor = None
    def __init__(self, ip, database, user, pas) -> None:
        self.ip = ip
        self.database = database 
        self.user = user 
        self.pas = pas

    def startConnection(self):
        try: 
            self.db_conn = mysql.connector.connect(host=self.ip, database=self.database, user=self.user, password=self.pas)

            if self.db_conn.is_connected():
            
                # Print the version of mqsql for testing the connection
                db_info = self.db_conn.get_server_info()
                print("Connected to MySQL Server version ", db_info, "\n")
                
        except Error as e:
            print("Error while connecting to MySQL: ", e)

    def query(self, query):
        cursor = self.db_conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        
        cursor.close()
        return records

    def stopConnection(self):
        if self.db_conn.is_connected():
            self.db_conn.close()
            print("MySQL connection is closed!")