
from crypt import methods
from flask import Flask, request, render_template, redirect, url_for
# from flask_restful import Resource, Api, reqparse
# from query import Connection
from models import category, person, interest


app = Flask(__name__)
# api = Api(app)

# Info
# host = '127.0.0.1'
# database = 'WBD'
# user =  'root'
# password = 'Nikolakolarov03!'

# Create object
# connection = Connection(host, database, user, password)
# connection.startConnection()

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

# add category
@app.route("/add-category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category_name = request.form.get("category_name")  
        # insert category in database
        cat = category.Category(category_name)
        cat.startConnection()
        tuple1 = (cat.category_name,)
        cat.insert_prepared_statement("""INSERT INTO Categories VALUES(NULL, %s)""", tuple1)
        cat.stopConnection()
        return redirect(url_for("index"))

    # if method is [GET], present the form
    return render_template("add_category.html")

    # return '''<h1>Arg1 is {}</h1>'''.format(category_name)#"query arguments example"

@app.route("/add-person", methods=["GET", "POST"])
def add_person():
    if request.method == "POST":
        #TODO: implement preference with dictionary
        preference = request.form.get("dropdown_preference")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        preference = int(preference)
        user = person.Person(first_name, last_name, preference)
        user.startConnection()
        tuple1 = (user.first_name, user.last_name, user.preference)
        user.insert_prepared_statement("INSERT INTO Person VALUES(NULL, %s, %s, %s)", tuple1)
        user.stopConnection()
        return redirect(url_for('index'))

    # if method is [GET], present the form
    return render_template("add_person.html")

@app.route("/add-interest", methods=["GET", "POST"])
def add_interest():
    if request.method == "POST":
        #TODO: implement preference with dictionary
        preference = request.form.get("dropdown_preference")
        preference = int(preference)
        user_id = request.form.get("user_id")
        user_id = int(user_id)
        tuple1 = (user_id, preference)
        interest_in = interest.Interest(user_id ,preference)
        interest_in.startConnection()
        interest_in.insert_prepared_statement("INSERT INTO Interested_in VALUES(NULL, %s, %s)")
        interest_in.stopConnection()
        return redirect(url_for('index'))

    # if method is [GET], present the form
    return render_template("add_interest.html")

@app.route("/add-visit", methods=["GET", "POST"])
def add_visit():
    if request.method == "POST":
        #TODO: implement preference with dictionary
        preference = request.form.get("dropdown_preference")
        preference = int(preference)
        user_id = request.form.get("user_id")
        user_id = int(user_id)
        interest_in = interest.Interest(user_id ,preference)
        tuple1 = (interest_in.user_id, interest_in.preference)
        interest_in.startConnection()
        interest_in.insert_prepared_statement("INSERT INTO Interested_in VALUES(NULL, %s, %s)", tuple1)
        interest_in.stopConnection()
        return redirect(url_for('index'))

    # if method is [GET], present the form
    return render_template("add_visit.html")

# form request.
@app.route("/add-museum", methods=["GET", "POST"])
def form_request():
    if request.method == "POST":
        museum_name = request.form.get("museum_name")
        museum_address = request.form.get("museum_adress")
        country = request.form.get("country_dropdown")
        rating = request.form.get("rating")
        museum_category = request.form.get("category_dropdown")
        museum_category = int(museum_category)
    
        return redirect(url_for('index'))

#         import requests
#         import urllib.parse

# address = 'Shivaji Nagar, Bangalore, KA 560001'
# url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

# response = requests.get(url).json()
# print(response[0]["lat"])
# print(response[0]["lon"])

    # if method is [GET], present the form
    return render_template("add_museum.html")

# receive JSON object
@app.route("/json-request", methods=["POST"])
def json_request():
    return "JSON request example"

    
if __name__ == "__main__":
    app.run(debug=True)

# connection.stopConnection()