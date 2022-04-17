from crypt import methods
from flask import Flask, request, render_template, redirect, session, url_for
from flask_session import Session
from models import category, person, interest, museum, profile_handler


# Utility function passed to the html template for calculation.
def round_num(x):
    return round(x)

app = Flask(__name__)
app.secret_key = "SuPerSecretKe7"
app.jinja_env.globals.update(round = round_num)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/version", methods=["GET"])
def version():
    return { "version": "0.0.1" }, 200

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("passwrd")
        password = str(password)
        username = str(username)


        result = profile_handler.ProfileHandler().log_in(username, password)
        if result != False:
            session["name"] = username
            session["id"] = result[0]
            session["fav_category"] = result[1]

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
    if not session.get("name"):
        return redirect(url_for('login'))
    
    __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage") #this object is not for insertion. It is created so the search method inside can be used.
    __museum.startConnection()
    results_ids = __museum.request_favourite(session.get("fav_category"), 30)

    results = []
    for r in results_ids:
        results.append(__museum.search_museum_by_id(r))
    __museum.stopConnection()

    _fields = ['id', 'name', 'country', 'address', 'rating', 'category', 'longitude', 'latitude', 'image_url']
    museum_dicts = [dict(zip(_fields, r[0])) for  r in results]
    item_list = [Item(i) for i in museum_dicts]
    museum_results = item_list

    msg = request.args.get("msg")
    return render_template("index.html", message = msg, museums = museum_results)

class Item:
    def __init__(self, vals):
        self.__dict__ = vals

museum_results = []

@app.route("/results", methods=["GET"])
def results():
    return render_template('results.html', museums = museum_results)

@app.route("/index", methods=['POST'])
def search_museum():
    # Search
    museum_keyword = request.form.get("search_museums")
    museum_keyword = str(museum_keyword)
    __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage") #this object is not for insertion. It is created so the search method inside can be used.
    __museum.startConnection()
    results = __museum.search_museum_by_name(museum_keyword, limit=100)
    __museum.stopConnection()
    #add field names
    _fields = ['id', 'name', 'country', 'address', 'rating', 'category', 'longitute', 'lantitute']
    museum_dicts = [dict(zip(_fields, r)) for r in results]
    #do some magic so it works.
    item_list = [Item(i) for i in museum_dicts]
    global museum_results
    museum_results = item_list
    return redirect(url_for('results'))

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
        user.insert_prepared_statement("INSERT INTO Person(id, first_name, user_name, most_liked_category_id) VALUES(NULL, %s, %s, %s)", tuple1)
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
        user_id = session.get("id")
        user_id = int(user_id)
        tuple1 = (user_id, preference)
        interest_in = interest.Interest(user_id ,preference)
        interest_in.startConnection()
        interest_in.insert_prepared_statement("INSERT INTO Interested_in VALUES(NULL, %s, %s)", tuple1)
        interest_in.stopConnection()
        return redirect(url_for('index'))

    # if method is [GET], present the form
    return render_template("add_interest.html")

# form request.
@app.route("/add-museum", methods=["GET", "POST"])
def add_museum():
    if request.method == "POST":
        museum_name = request.form.get("museum_name")
        museum_address = request.form.get("museum_adress")
        country = request.form.get("country_dropdown")
        rating = request.form.get("rating")
        rating = float(rating)
        rating = ((1-0)*(rating-0)/5-0)+0
        rating = round(rating, 2)
        print(rating)
        museum_category = request.form.get("category_dropdown")
        museum_category = int(museum_category)
        museum_obj = museum.Museum(museum_name.upper(), museum_address, country, rating, museum_category)
        tuple1 = (museum_obj.museum_name, museum_obj.country, museum_obj.museum_address, museum_obj.rating, museum_obj.museum_category)
        museum_obj.startConnection()
        query = "INSERT INTO Museums VALUES(NULL, %s, %s, %s, %s, %s, 0, 0, NULL, NULL)"
        museum_obj.insert_prepared_statement(query, tuple1)
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
    return app.send_static_file('favicon.ico')

# receive JSON object
@app.route("/json-request", methods=["POST"])
def json_request():
    return "JSON request example"

    
if __name__ == "__main__":
     app.run(debug=True)