from query import Connection
from models import consts
import bcrypt

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
# connection.startConnection()
class ProfileHandler:
    def log_in(self, username, password):
        password = password.encode('utf8')

        connection.startConnection()
        query = "SELECT id, most_liked_category_id, hashed_password FROM Person WHERE username = \"{}\"".format(username)
        result = connection.query(query)
        id = result[0][0]
        fav_category = result[0][1]
        hashed_password = result[0][2]
        hashed_password = hashed_password.encode('utf8')

        if bcrypt.checkpw(password, hashed_password):
            print("match")
            connection.stopConnection()
            return [id, fav_category]
        else:
            connection.stopConnection()
            return False

    def register(self, first_name: str, sur_name: str, username: str, password: str, fav_category: int):
        password = password.encode('utf8')

        connection.startConnection()
        # Check for existing entry
        query_check = "SELECT EXISTS(SELECT 1 FROM Person WHERE username = \"{}\")".format(username)
        result = connection.query(query_check)
        result = result[0][0]
        if result == 1:
            print("Username already exists")
            return

        salt = bcrypt.gensalt(rounds=14)
        hashed_password = bcrypt.hashpw(password, salt)
        hashed_password = hashed_password.decode('utf8')

        query = "INSERT INTO Person VALUE (NULL, %s, %s, %s, %s, %s);"
        tuple1 = (first_name, sur_name, username, hashed_password, str(fav_category))
        connection.insert_prepared_statement(query, tuple1)

        connection.stopConnection()