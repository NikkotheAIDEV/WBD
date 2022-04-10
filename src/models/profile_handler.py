from query import Connection
from models import consts
import bcrypt

connection = Connection(consts.HOST, consts.DATABASE, consts.USER, consts.PASSWORD)
# connection.startConnection()
class ProfileHandler:
    def log_in(self, username, password):
        password = password.encode('utf8')

        connection.startConnection()
        query = "SELECT hashed_password FROM Person WHERE username = \"{}\"".format(username)
        hashed_password = connection.query(query)
        hashed_password = hashed_password[0][0]
        hashed_password = hashed_password.encode('utf8')

        if bcrypt.checkpw(password, hashed_password):
            print("match")
            connection.stopConnection()
            return True
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

        query = "INSERT INTO Person VALUE (NULL, \"{}\", \"{}\", \"{}\", \"{}\", {});".format(first_name, sur_name, username, hashed_password, fav_category)
        connection.insert_prepared_statement(query, None)

        connection.stopConnection()

# TESTS
# profile = ProfileHandler()
# profile.register("Vladislav", "Terziev", "VladiT", "Terziev123", 3)
# profile.register("Ivan", "Terziev", "Vankata38", "Terziev123", 3)

# profile.log_in("VladiT", "Terziev123")
# profile.log_in("Vankata38", "Terziev123")

# connection.stopConnection()