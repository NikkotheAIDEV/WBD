import mysql.connector
from mysql.connector import Error

class Connection:
    db_conn = None

    def __init__(self, ip, database, user, pas) -> None:
        self.ip = ip
        self.database = database 
        self.user = user 
        self.pas = pas

    def startConnection(self):
        try: 
            global db_conn
            db_conn = mysql.connector.connect(host=self.ip, database=self.database, user=self.user, password=self.pas)

            if db_conn.is_connected():
            
                # Print the version of mqsql for testing the connection
                db_info = db_conn.get_server_info()
                print("Connected to MySQL Server version ", db_info, "\n")
                
        except Error as e:
            print("Error while connecting to MySQL: ", e)

    def query(self, query):
        global db_conn
        cursor = db_conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        
        cursor.close()
        return records

    def insert(self, query):
        global db_conn
        cursor = db_conn.cursor()
        cursor.execute(query)
        db_conn.commit()
        
        cursor.close()

    def stopConnection(self):
        if db_conn.is_connected():
            db_conn.close()
            print("MySQL connection is closed!")