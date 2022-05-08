from query import Connection
from models import consts, interest
import bcrypt

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
# connection.startConnection()
class ProfileHandler:
    def log_in(self, username, password):
        password = password.encode('utf8')

        connection.startConnection()
        query = "SELECT id, most_liked_category_id, hashed_password FROM Person WHERE username = \"{}\"".format(username)
        result = connection.query(query)

        if result == []:
            return False

        # Find user info
        user_id = result[0][0]
        fav_category = result[0][1]
        query_interested_in = "SELECT category_id FROM Interested_in WHERE person_id = {};".format(user_id)
        interested_in_results = connection.query(query_interested_in)

        # Find interested in categories for this user
        interested_in_arr = []
        for index, i in enumerate(interested_in_results):
            interested_in_arr.append(interested_in_results[index][0])

        # Find and check password
        hashed_password = result[0][2]
        hashed_password = hashed_password.encode('utf8')

        if bcrypt.checkpw(password, hashed_password):
            print("match")
            connection.stopConnection()
            return [user_id, fav_category, interested_in_arr]
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