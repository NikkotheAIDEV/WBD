
from flask import Flask
from flask_restful import Resource, Api, reqparse
from query import Connection


app = Flask(__name__)
api = Api(app)

# Info
host = '127.0.0.1'
database = 'WBD'
user =  'root'
password = 'Nikolakolarov03!'

# Create object
connection = Connection(host, database, user, password)
connection.startConnection()

# query = "SELECT * FROM Mu"
# records = connection.query(query)
# print("rows = " + str(len(records)) + "\n")
# for row in records:
#     print("ID = ", row[0])
#     print("Name = "+ str(row[1])+ "\n")

connection.stopConnection()

class Museums(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('arg1', type = str, help="Only integers allowed",  required=True)

        args = parser.parse_args()
        # print(args['arg1'])
        return {"message": "Success", "args_received": args['arg1']}, 200

api.add_resource(Museums, '/museum')

@app.route('/hello', methods=['GET'])
def index():
    return "Hello from hello!"

    
if __name__ == "__main__":
    app.run(debug=True)