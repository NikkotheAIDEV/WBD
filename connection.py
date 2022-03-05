import mysql.connector
from mysql.connector import Error

try:
    # Info
    host = 'localhost'
    database = 'Airport'
    user =  'root'
    password = 'Terziev123'

    # Connect
    connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

    if connection.is_connected():
        
        # Print the version of mqsql for testing the connection
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)

        # Run a query
        query = "SELECT * FROM Passenger"
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        print("Total number of rows: ", cursor.rowcount)

        # Print the query results
        print("\n Printing every row")
        for row in records:
            print("ID_psg = ",row[0])
            print("Name = ", row[1])

# Handle errors
except Error as e:
    print("Error while connecting to MySQL: ", e)

# Close the connection
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed!")