"""
    main.py - This is the Flask application's python file
"""
# File Imports
import google.oauth2.id_token
import datetime
import requests
import logging
import json
import os

from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from firebase_admin import credentials, firestore, initialize_app
from google.auth.transport import requests as grequests
from google.cloud import datastore
from bson.json_util import dumps
from pymongo import MongoClient

# Google Cloud set up for local development. Comment out for live cloud deployment
os.environ.setdefault("GCLOUD_PROJECT", "game-store-ad")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ajvea\code\ad\advanced-development-assignment-AJVEATS\venv\application_default_credentials.json"

firebase_request_adapter = grequests.Request()

# Google Cloud Datastore client connection
datastore_client = datastore.Client()

app = Flask(__name__)

app.config["SECRET_KEY"] = "6333292761132459"

# MonogoDB Connection for the Games collection in the GameStoreDB cluster
cluster = MongoClient("mongodb+srv://AJVEATS:alexTest@gamestoredb.gaxxodr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["GameStoreDB"]
collection = db["Games"]


"""
    get_games function connects to the get_mongodb_games Google Cloud function that returns all of the games that are
    stored in the MongoDB 'Games' collection.

    :return data: All the game data returned from the get_mongodb_games cloud function
"""
def get_games():
    # Url for the get_mongodb_games Google Cloud Function
    url = "https://europe-west2-game-store-ad.cloudfunctions.net/get_mongodb_games"

    uResponse = requests.get(url)
    jResponse = uResponse.text
    data = json.loads(jResponse)

    return data


"""
    get_single_game function connects to the get_mongodb_single_game Google Cloud function with the game's slug, which returns the data for
    the game selected by the user.

    :param slug: The selected game's slug
    :return data: the game data returned from the get_mongodb_single_game cloud function
"""
def get_single_game(slug):
    # Url for the get_single_game Google Cloud Function which includes the selected games slug
    url = ("https://europe-west2-game-store-ad.cloudfunctions.net/get_mongodb_single_game?slug=" + slug)

    uResponse = requests.get(url)
    jResponse = uResponse.text
    data = json.loads(jResponse)

    return data


"""
    delete_game() function connects to the delete_mongodb_game Google Cloud function with the game's slug that returns the data for
    the game selected by the user from the MongoDB 'Games' collection.

    :param slug: The selected game's slug
    :return: Returns a confirmation string
"""
def delete_game(slug):
    # Url for the delete_mongodb_game Google Cloud Function which includes the selected games slug which is being deleted
    url = ("https://europe-west2-game-store-ad.cloudfunctions.net/delete_mongodb_game?slug=" + slug)
    uResponse = requests.get(url)
    uResponse

    return "game has been deleted"


"""
    add_user_details() function adds the inputted user details to the Google Cloud
    datastore

    :param gameName: The user's gamertag
    :param favouriteGame: The user's favourite game
    :param favouriteGenre: The user's favourite genre
    :param platform: The user's platform
    :param uid: The user's firebase authentication user id
    :param email: The user's firebase authentication email
    :param name: The user's firebase authentication email
    :return: Returns a confirmation string
"""
def add_user_details(gameName, favouriteGame, favouriteGenre, platform, uid, email, name):
    entity = datastore.Entity(key=datastore_client.key('UserID', uid, 'userDetails'))
    entity.update({
        "name": name,
        "email": email,
        "gamertag": gameName,
        "favouriteGame": favouriteGame,
        "favouriteGenre": favouriteGenre,
        "platform": platform,
        "timestamp": datetime.datetime.now()
    })

    datastore_client.put(entity)

    return "User details have been added"


"""
    get_user_details() function gets the user's most current data from the google cloud datastore.
    If they have no data userData is set to null otherwise it is set the user's most current 
    data.

    :param uid: The user's user id
    :param limit: The query limit
    :return userData: the user's most current information or null 
"""
def get_user_details(uid, limit):
    ancestor = datastore_client.key('UserID', uid)
    query = datastore_client.query(kind='userDetails', ancestor=ancestor)
    query.order = ['-timestamp']

    query_results = list(query.fetch())

    # print(len(query_results)) # For testing, displays userData to console

    if len(query_results) == 0:
        userData = "null"
    else:
        userData = query.fetch(limit=limit)

    # print(userData) # For testing, displays userData to console

    return userData


"""
    delete_user_info() function deletes all the user's data from the google cloud datastore.

    :param uid: The user's user id
    :return: Returns a confirmation string
"""
def delete_user_info(uid):
    print("delete user has been initiated with the uid of " + uid)
    
    ancestor = datastore_client.key("UserID", uid)
    query = datastore_client.query(kind='userDetails', ancestor=ancestor)
    data = query.fetch()
    datastore_client.delete_multi(data)

    return "User's info has been deleted"


"""
    deleteGame() function is passed in with the slug of the game that has been selected to be deleted. API for the 
    '/api/game/<slug>' path, slug being the selected game. It calls on the delete_game() function and passes in the 
    selected game's slug, which will delete the game from the MongoDB 'Games' collection.

    :param slug: The slug of the game being deleted
    :return: Returns a confirmation string
"""
@app.route("/api/game/<slug>", methods=["DELETE"])
def deleteGame(slug):
    delete_game(slug)
    
    return "The game has been deleted"


"""
    delteFromCart() function is passed in with the slug of the game that has been selected to be deleted. API for the 
    '/api/deleteCartItem/<game>/<uid>' path, game being the selected game and uid being the user's userID. It deletes
    that specific games basket entry from the 'Cart' MongoDB collection

    :param game: The Game name that is being deleted
    :param uid: The user's userID
    :return: Returns a confirmation string
"""
@app.route("/api/deleteCartItem/<game>/<uid>", methods=["DELETE"])
def deleteFromCart(game, uid):
    collection = db["Cart"]
    query = { 'game' : {"$eq": game}, 'userID' : {"$eq": uid}}
    collection.delete_one({"$and": [query]})
    return "The game has been removed from your basket"


@app.route("/api/clearBasket/<uid>", methods=["DELETE"])
def clearCart(uid):
    print("clearCart() has been initiated with " + uid)
    collection = db["Cart"]
    
    query = { 'userID' : {"$eq": uid}}
    collection.delete_many({"$and": [query]})
    return "The game has been removed from your basket"


@app.route("/api/purchase/<order>", methods=["POST"])
def purchase(order):
    
    collection = db["Orders"]
    order_json = json.loads(order)  
    # print(order)
    
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    
    order_json['email'] = claims['email']
    order_json['name'] = claims['name']
    order_json['timestamp'] = datetime.datetime.now()
    
    print(order_json['userID'])

    collection.insert_one(order_json)
    clearCart(order_json['userID'])

    return "purchase has been made"


"""
    deleteUser() function is passed in the user id of the user. API for the '/api/userInfo/<uid>' path, uid being the 
    user's user id. It calls on the delete_user_info() function and passes in the user's user id, which will delete
    the users data from the Google Cloud Datastore

    :param uid: The user's user id
    :return: Returns a confirmation string
"""
@app.route("/api/userInfo/<uid>", methods=["DELETE"])
def deleteUser(uid):
    # print("delete api reached") # For Testing
    delete_user_info(uid)
    
    return "User info has been deleted"


"""
    add_to_cart() function is passed in with the user id of the user and the slug of the game that they want to add to
    their cart. It then adds the data to the MongoDB collection 'Cart'.

    :param slug: The slug of the game selected by the user
    :param uid: The user's user id
    :return: Returns a confirmation string
"""
@app.route("/api/addToCart/<slug>/<uid>/<price>", methods=["POST"])
def addToCart(slug, uid, price):
    # print("Passed in slug is " + slug) # For Testing
    # print("Passed in uid is " + uid) # For Testing
    # print("Passed in price is " + price) # For Testing
    collection = db["Cart"]
    new_cart_item_json = {
        "userID": uid,
        "game": slug,
        "price": price,
        "timestamp": datetime.datetime.now(),
    }

    collection.insert_one(new_cart_item_json)
    return "Game has been added to you cart, this has been updated in the database"


"""
    root() function for rendering the 'root.html' template at route '/'.
"""
@app.route("/")
def root():
    return render_template("/root.html")


"""
    index() function for rendering the 'index.html' template at route '/home' and '/index'
    with data from the get_games() function
"""
@app.route("/index")
@app.route("/home")
def index():
    data = get_games()
    return render_template("/index.html", data=data)


"""
    games() function for rendering the 'games.html' template at route '/games' with data from the 
    get_games() function
"""
@app.route("/games")
def games():
    data = get_games()
    return render_template("/games.html", data=data)


"""
    single_game() function for rendering the 'game.html' template at route '/<slug>'
    with data from the get_single_game() function passing in the selected games slug.

    :param slug: The slug of the selected game
"""
@app.route("/<slug>")
def single_game(slug):
    data = get_single_game(slug)
    return render_template("/game.html", data=data)


"""
    basket() function for rendering the 'basket.html' template at route '/basket' with data which is
    all of the games in the user basket. It also totals all of the game prices. 
    
"""
@app.route("/basket")
def basket():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    uid = claims['user_id']
    collection = db["Cart"]
    # Gets game data by the userID from Mongodb
    myCursor = None
    cart_query = {"userID": {"$eq": uid}}
    myCursor = collection.find({"$and": [cart_query]}).sort("timestamp", -1)
    list_cur = list(myCursor)
    # print(list_cur[1]) # For Testing
    total = 00.00
    for game in list_cur:
        total = total + float(game.get('price')[1: ])
        total = round(total, 2)

    # print(total) # For Testing
    return render_template("/basket.html", data=list_cur, total=total, uid=uid)


"""
    about() function for rendering the 'about.html' template at route '/about'.
"""
@app.route("/about")
def about():
    return render_template("/about.html")


"""
    account() function for rendering the 'account.html' template at route '/account' with data from the 
    get_user_details() function passing in the user's id which is taken from the firebase 
    authentication.
"""
@app.route("/account")
def account():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    data = get_user_details(claims['user_id'], 1)
    return render_template("/account.html", data=data, user_data=claims)


"""
    account_info() function for rendering the 'account.html' template at route '/account' with data from the 
    get_user_details() function passing in the user's id which is taken from the firebase 
    authentication. If the form sends a post request is collects the data entered into the form, deletes the 
    user's last entry from the Google Cloud Datastore with the delete_user_info() function passing in the 
    user's id. It then adds the submitted data to the datastore with the add_user_details() functions passing
    in the forms submitted data.
"""
@app.route("/account-info", methods=["GET", "POST"])
def account_info():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)

    user_data = get_user_details(claims['user_id'], 1)

    if request.method == "POST":
        gameName = request.form["gamertag"]
        game = request.form["favouriteGame"]
        genre = request.form["favouriteGenre"]
        platform = request.form["platform"]

        delete_user_info(claims['user_id'])
        add_user_details(gameName, game, genre, platform, claims['user_id'], claims["email"], claims["name"])

        return redirect(url_for('account'))

    data = get_games()
    return render_template("/account_info.html", data=data, user_data=user_data)


"""
    orders() function for rendering the 'orders.html' template at route '/order'. It displays the users
    orders from the MongoDB 'Orders' collection
"""
@app.route("/orders")
def orders():
    id_token = request.cookies.get("token")
    claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
    uid = claims['user_id']
    # print(uid)
    collection = db["Orders"]
    # Gets game data by the userID from Mongodb
    myCursor = None
    # order_query = {"userID": {"$eq": uid}}
    # myCursor = collection.find({"$and": [order_query]})
    cart_query = {"userID": uid}
    myCursor = collection.find(cart_query)
    list_cur = list(myCursor)
    print(list_cur)
    for x in myCursor:
        print(x)

    return render_template("/orders.html", data=list_cur)


"""
    add_game_page() function for rendering the 'store_admin.html' template at route '/store-admin' with data from the 
    get_games() function. If the form on the page submits a POST request, the submitted information is passed 
    into the create_mongodb_games cloud function which adds the submitted information to the MongoDB 'Games'
    collection
"""
@app.route("/store-admin", methods=["GET", "POST"])
def add_game_page():

    if request.method == "POST":
        slug = request.form["gameSlug"]
        name = request.form["gameName"]
        release = request.form["gameReleaseDate"]
        genre = request.form["gameGenre"]
        rating = request.form["gameRating"]
        ageRating = request.form["gameAgeRating"]
        image = request.form["gameImage"]
        price = request.form["gamePrice"]
        description = request.form["gameDescription"]

        new_game_json = {
            "slug": slug,
            "name": name,
            "released": release,
            "genre": genre,
            "rating": rating,
            "age_rating": ageRating,
            "image": image,
            "price": price,
            "description": description,
        }

        new_game_string = json.dumps(new_game_json)

        url = ("https://europe-west2-game-store-ad.cloudfunctions.net/create_mongodb_game?game_data=" + new_game_string)

        uResponse = requests.get(url)
        uResponse

    data = get_games()

    return render_template("/store_admin.html", data=data)

"""
    editGames() function for rendering the 'edit_games.html' template at route '/edit-games'
    with data from the get_games() function.
"""
@app.route("/edit-games")
def editGames():
    data = get_games()
    return render_template("/edit_games.html", data=data)


"""
    editGame() function takes in the data submitted by the pages form and passes the data
    into the update_mongodb_game Google Cloud function, which will update the game within
    the 'Games' Collection from the MonogoDB. The games data is pulled in from the MonogoDB
    and passed into the template render.
"""
@app.route("/edit-game/<slug>", methods=["GET", "POST"])
def editGame(slug):

    if request.method == "POST":
        newSlug = request.form["gameSlug"]
        name = request.form["gameName"]
        release = request.form["gameReleaseDate"]
        genre = request.form["gameGenre"]
        rating = request.form["gameRating"]
        ageRating = request.form["gameAgeRating"]
        image = request.form["gameImage"]
        price = request.form["gamePrice"]
        description = request.form["gameDescription"]

        url = (
            "https://europe-west2-game-store-ad.cloudfunctions.net/update_mongodb_game?oldSlug="
            + slug
            + "&newSlug="
            + newSlug
            + "&name="
            + name
            + "&release="
            + release
            + "&genre="
            + genre
            + "&rating="
            + rating
            + "&ageRating="
            + ageRating
            + "&image="
            + image
            + "&price="
            + price
            + "&description="
            + description
        )
        uResponse = requests.get(url)
        uResponse

    data = get_single_game(slug)

    return render_template("/edit_game.html", data=data)

"""
    Error handling for 500 errors
"""
@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception("An error occurred during a request.")
    return "An internal error occurred.", 500

"""
    Error handling for 404 errors 
"""
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/404.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
