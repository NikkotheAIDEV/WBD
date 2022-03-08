
from flask import Flask, request, render_template, redirect, url_for
# from flask_restful import Resource, Api, reqparse
from query import Connection
from models import category


app = Flask(__name__)
# api = Api(app)

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

# class Museums(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('arg1', type = str, help="Only integers allowed",  required=True)

#         args = parser.parse_args()
#         # print(args['arg1'])
#         return {"message": "Success", "args_received": args['arg1']}, 200

# api.add_resource(Museums, '/museum')

@app.route("/version", methods=["GET"])
def version():
    # if connection:
    #     return "Successfully connected to db"
    return { "version": "0.0.1" }, 200
    #  return render_template("add_museum.html")

@app.route("/", methods=["GET"])
def index():
    msg = request.args.get("msg")

    # if connection:
    #     return "Successfully connected to db"
    # return { "version": "0.0.1" }, 200
    return render_template("index.html", message = msg)

# regular request with arguments(e.g. website.com/query-request?arg1=argument1)
@app.route("/query-request")
def query_request():
    arg1 = request.args.get("arg1")
    return '''<h1>Arg1 is {}</h1>'''.format(arg1)#"query arguments example"

# form request.
@app.route("/form-request", methods=["GET", "POST"])
def form_request():
    if request.method == "POST":
        museum_name = request.form.get("museum_name")
        museum_address = request.form.get("museum_adress")
        # return "Hello", 200
        return redirect(url_for('index'))

    # if method id [GET], present the form
    # return '''
    # <form method = "POST">
    # <div><label>Museum name: <input type="text" name="museum_name"></label></div>
    # <div><label>Adress: <input type="text" name="museum_adress"></label></div>
    # <input type="submit" value = "Submit">
    # </form>'''
    return render_template("add_museum.html")

# receive JSON object
@app.route("/json-request", methods=["POST"])
def json_request():
    return "JSON request example"

    
if __name__ == "__main__":
    app.run(debug=True)

connection.stopConnection()