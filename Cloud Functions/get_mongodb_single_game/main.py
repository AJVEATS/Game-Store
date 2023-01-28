import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json


def get_mongodb_single_game(request):
    cluster = MongoClient(
        "mongodb+srv://AJVEATS:alexTest@gamestoredb.gaxxodr.mongodb.net/?retryWrites=true&w=majority"
    )
    db = cluster["GameStoreDB"]
    collection = db["Games"]

    passed_slug = request.args.get("slug")

    # Gets game data by slug from Mongodb
    myCursor = None
    # Query to get the game by it's slug
    game_query = {"slug": {"$eq": passed_slug}}
    myCursor = collection.find({"$and": [game_query]})
    list_cur = list(myCursor)
    # print(list_cur)
    json_data = dumps(list_cur)
    return json_data
