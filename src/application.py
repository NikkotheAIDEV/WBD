from flask import Flask, request, render_template, redirect, session, url_for
from flask_session import Session
from models import category, person, interest, museum, profile_handler
from crypt import methods
import random

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

@app.route("/", methods=["GET", "POST"])
def login():
    if not session.get("name"):
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
                session["interested_in"] = result[2]

                return redirect(url_for('index'))
        return render_template("login.html")
    else:
        return redirect(url_for('index'))

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/signup", methods=["GET", "POST"])
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

class Item:
    def __init__(self, vals):
        self.__dict__ = vals

museum_results = []
museum_detail = []
ratings_given_ids = []

@app.route("/results", methods=["GET","POST"])
def results():
    if request.method == "POST":
        if request.form['btn_id'] == 'detailed_view':
            __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage", "empty")
            __museum.startConnection()
            
            museum_id = request.form.get("museum_id")
            result_museum = __museum.search_museum_by_id(museum_id)
            __museum.stopConnection()

            _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitute', 'lantitute', "image_url"]
            museum_dict = dict(zip(_fields, result_museum[0]))
            global museum_detail
            museum_detail = Item(museum_dict)

            return redirect(url_for('detailed'))

    if request.method == "GET":
        return render_template('results.html', museums = museum_results)

@app.route("/detailed", methods=["GET",'POST'])
def detailed():
    if request.method == "GET":
        if museum_results == []:
            return redirect(url_for("index"))
        else:
            global museum_detail
            return render_template('detailed_view.html', museum = museum_detail)

    if request.method == "POST":
        __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage", "empty")
        __museum.startConnection()
        
        rating = 0
        museum_id = request.form.get("museum_id")

        global ratings_given_ids
        ratings_given_ids.clear()
        user_id = session.get("id")
        query = "SELECT museum_id FROM Ratings WHERE person_id = {};".format(user_id)
        results = __museum.query(query)

        for index, i in enumerate(results):
            ratings_given_ids.append(results[index][0])

        if request.form["rating"] == "1":
            rating = 1
        elif request.form["rating"] == "2":
            rating = 2
        elif request.form["rating"] == "3":
            rating = 3
        elif request.form["rating"] == "4":
            rating = 4
        elif request.form["rating"] == "5":
            rating = 5

        # Query old values
        query = "SELECT avg_rating, number_of_ratings FROM Museums WHERE id = {}".format(museum_id)
        results = __museum.query(query)

        # Get old values
        avg_rating = results[0][0]
        avg_rating = ((5-1)*(avg_rating-0)/1-0)+1
        number_of_ratings = results[0][1]

        if int(museum_id) not in ratings_given_ids:

            # Calculate new values
            prod = number_of_ratings * avg_rating
            number_of_ratings += 1
            new_rating = (prod + rating) / number_of_ratings
            new_rating = ((1-0) * (new_rating - 0)/(5 - 0) + 0)

            # Update db
            update_query = "UPDATE Museums SET avg_rating = %s, number_of_ratings = %s WHERE id = %s"
            tuple1 = (new_rating, number_of_ratings, museum_id)
            __museum.insert_prepared_statement(update_query, tuple1)
            
            # Update current page
            result_museum = __museum.search_museum_by_id(museum_id)
            _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitute', 'lantitute', "image_url"]
            museum_dict = dict(zip(_fields, result_museum[0]))
            museum_detail = Item(museum_dict)
            
            # Update Ratings table
            ratings_given_ids.append(int(museum_id))
            add_rating_query = "INSERT INTO Ratings VALUE(NULL, %s, %s, %s);"
            tuple1 = (user_id, museum_id, rating)
            __museum.insert_prepared_statement(add_rating_query, tuple1)
            __museum.stopConnection()

            # Return templa/te
            return redirect(url_for('detailed'))

        else:

            # Get old rating from Ratings
            get_rating_query = "SELECT rating FROM Ratings Where person_id = {} AND museum_id = {}".format(user_id, museum_id)
            results = __museum.query(get_rating_query)
            old_rating = results[0][0]

            # Calculate new values
            prod = number_of_ratings * avg_rating
            new_rating = (prod + rating - old_rating) / number_of_ratings
            new_rating = ((1-0) * (new_rating - 0)/(5 - 0) + 0)

            # Update db
            update_query = "UPDATE Museums SET avg_rating = %s, number_of_ratings = %s WHERE id = %s"
            tuple1 = (new_rating, number_of_ratings, museum_id)
            __museum.insert_prepared_statement(update_query, tuple1)

            # Update current page
            result_museum = __museum.search_museum_by_id(museum_id)
            _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitute', 'lantitute', "image_url"]
            museum_dict = dict(zip(_fields, result_museum[0]))
            museum_detail = Item(museum_dict)

            update_ratings_query = "UPDATE Ratings SET rating = %s Where person_id = %s AND museum_id = %s"
            tuple1 = (rating, user_id, museum_id)
            __museum.insert_prepared_statement(update_ratings_query, tuple1)
            __museum.stopConnection()

            return redirect(url_for('detailed'))


@app.route("/index", methods=['GET','POST'])
def index():
    if request.method == "GET":
        if not session.get("name"):
            return redirect(url_for('login'))
        
        __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage", "empty") #this object is not for insertion. It is created so the search method inside can be used.
        __museum.startConnection()

        results_ids = []
        if session.get("interested_in") == []:
            results_ids.extend(__museum.request_favourite(session.get("fav_category"), 30))
            random.shuffle(results_ids)
        else:
            results_ids.extend(__museum.request_favourite(session.get("fav_category"), 20))
            results_ids.extend(__museum.request_interested(session.get("interested_in"), 10))
            random.shuffle(results_ids)

        results = []
        for r in results_ids:
            results.append(__museum.search_museum_by_id(r))
        __museum.stopConnection()

        _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitude', 'latitude', 'image_url']
        museum_dicts = [dict(zip(_fields, r[0])) for  r in results]
        item_list = [Item(i) for i in museum_dicts]
        global museum_results
        museum_results = item_list

        msg = request.args.get("msg")
        return render_template("index.html", message = msg, museums = museum_results)
    
    if request.method == "POST":
        if request.form['btn_id'] == 'search':
            museum_keyword = request.form.get("search_museums")
            museum_keyword = str(museum_keyword)
            __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage", "empty") #this object is not for insertion. It is created so the search method inside can be used.
            __museum.startConnection()
            results = __museum.search_museum_by_name(museum_keyword, limit=100)
            __museum.stopConnection()
            #add field names
            _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitute', 'lantitute', "image_url"]
            museum_dicts = [dict(zip(_fields, r)) for r in results]
            #do some magic so it works.
            item_list = [Item(i) for i in museum_dicts]
            museum_results = item_list
            return redirect(url_for('results'))

        if request.form['btn_id'] == 'detailed_view':
            __museum = museum.Museum("some", "random", "info", "for", "object", "for", "methods", "usage", "empty")
            __museum.startConnection()
            
            museum_id = request.form.get("museum_id")
            result_museum = __museum.search_museum_by_id(museum_id)
            __museum.stopConnection()

            _fields = ['id', 'name', 'country', 'address', 'rating', 'number_of_ratings', 'category', 'longitute', 'lantitute', "image_url"]
            museum_dict = dict(zip(_fields, result_museum[0]))
            global museum_detail
            museum_detail = Item(museum_dict)

            return redirect(url_for('detailed'))

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
        museum_category = request.form.get("category_dropdown")
        museum_category = int(museum_category)
        museum_image_url = request.form.get("museum_url")
        museum_obj = museum.Museum(museum_name.upper(), museum_address, country, rating, "NULL", museum_category, "NULL", "NULL", museum_image_url)
        tuple1 = (museum_obj.museum_name, museum_obj.country, museum_obj.museum_address, museum_obj.rating, museum_obj.number_of_ratings, museum_obj.museum_category, museum_obj.image_url)
        museum_obj.startConnection()
        query = "INSERT INTO Museums VALUES(NULL, %s, %s, %s, %s, %s, %s, NULL, NULL, %s)"
        museum_obj.insert_prepared_statement(query, tuple1)
        museum_obj.stopConnection()
    
        return redirect(url_for('index'))
    return render_template("add_museum.html")

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

# receive JSON object
@app.route("/json-request", methods=["POST"])
def json_request():
    return "JSON request example"


if __name__ == "__main__":
     app.run(debug=True)