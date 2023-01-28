import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json


def create_mongodb_single_game(request):
    cluster = MongoClient(
        "mongodb+srv://AJVEATS:alexTest@gamestoredb.gaxxodr.mongodb.net/?retryWrites=true&w=majority"
    )
    db = cluster["GameStoreDB"]
    collection = db["Games"]

    new_game_json = json.loads(request.args.get("game_data"))

    collection.insert_one(new_game_json)

    return "Game has been added"
