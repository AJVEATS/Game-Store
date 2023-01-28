import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json


def get_mongodb_games(request):
    cluster = MongoClient(
        "mongodb+srv://AJVEATS:alexTest@gamestoredb.gaxxodr.mongodb.net/?retryWrites=true&w=majority"
    )
    db = cluster["GameStoreDB"]
    collection = db["Games"]

    myCursor = None
    myCursor = collection.find()
    list_cur = list(myCursor)
    # print(list_cur)
    json_data = dumps(list_cur)
    return json_data
