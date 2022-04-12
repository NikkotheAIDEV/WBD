from crypt import methods
# from WBD.src.models.profile_handler import ProfileHandler
from flask import Flask, request, render_template, redirect, session, url_for
# from flask_restful import Resource, Api, reqparse
# from query import Connection
from models import category, person, interest, museum, profile_handler


# Utility function passed to the html template for calculation.
def round_num(x):
    return round(x)

app = Flask(__name__)
app.secret_key = "SuPerSecretKe7"
app.jinja_env.globals.update(round = round_num)

@app.route("/version", methods=["GET"])
def version():
    #if connection:
    #return "Successfully connected to db"
    return { "version": "0.0.1" }, 200
    #return render_template("add_museum.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("passwrd")
        password = str(password)
        username = str(username)


        result = profile_handler.ProfileHandler().log_in(username, password)
        if result:
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        preference = request.form.get("dropdown_preference")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("passwrd")
        password = str(password)
        first_name = str(first_name)
        last_name = str(last_name)
        username = str(username)
        preference = int(preference)

        profile_handler.ProfileHandler().register(first_name, last_name, username, password, preference)
        return redirect(url_for('login'))

    return render_template("signup.html")

@app.route("/index", methods=["GET"])
def index():
    msg = request.args.get("msg")

    # if connection:
    #return "Successfully connected to db"
    #return { "version": "0.0.1" }, 200
    return render_template("index.html", message = msg)

class Item:
    def __init__(self, vals):
        self.__dict__ = vals

museum_results = []

@app.route("/results", methods=["GET"])
def results():
    museums = request.args.get("museums_dicts")
    return render_template('results.html', museums = museum_results)

@app.route("/index", methods=['POST'])
def search_museum():
    museum_keyword = request.form.get("search_museums")
    museum_keyword = str(museum_keyword)
    __museum = museum.Museum("some", "random", "info", "for", "object") #this object is not for insertion. It is created so the search method inside can be used.
    __museum.startConnection()
    results = __museum.search_muesums(museum_keyword, limit=100) 
    __museum.stopConnection()
    #add field names
    _fields = ['id', 'name', 'country', 'address', 'rating', 'category', 'longitute', 'lantitute']
    museum_dicts = [dict(zip(_fields, r)) for r in results]
    #do some magic so it works.
    item_list = [Item(i) for i in museum_dicts]
    global museum_results
    museum_results = item_list
    return redirect(url_for('results'))#museums_dicts=museum_dicts))



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
def add_museum():
    if request.method == "POST":
        museum_name = request.form.get("museum_name")
        museum_address = request.form.get("museum_adress")
        country = request.form.get("country_dropdown")
        rating = request.form.get("rating")
        museum_category = request.form.get("category_dropdown")
        museum_category = int(museum_category)
        museum_obj = museum.Museum(museum_name.upper(), museum_address, country, rating, museum_category)
        tuple1 = (museum_obj.museum_name, museum_obj.country, museum_obj.museum_address, museum_obj.rating, museum_obj.museum_category)
        museum_obj.startConnection()
        museum_obj.insert_prepared_statement("INSERT INTO Museums VALUES(NULL, %s, %s, %s, %s, %s, 0, 0)", tuple1)
        museum_obj.stopConnection()
    
        return redirect(url_for('index'))

#         import requests
#         import urllib.parse

# address = 'Shivaji Nagar, Bangalore, KA 560001'
# url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

# response = requests.get(url).json()
# print(response[0]["lat"])
# print(response[0]["lon"])
    # print("National Museum".upper())
    # if method is [GET], present the form
    return render_template("add_museum.html")


@app.route('/favicon.ico') 
def favicon(): 
    return

# receive JSON object
@app.route("/json-request", methods=["POST"])
def json_request():
    return "JSON request example"

    
if __name__ == "__main__":
     app.run(debug=True)
    # app.run(host='127.0.0.1')

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

# connection.stopConnection()