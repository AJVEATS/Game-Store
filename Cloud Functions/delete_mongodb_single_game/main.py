import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json


def delete_mongodb_single_game(request):
    cluster = MongoClient(
        "######"
    )
    db = cluster["GameStoreDB"]
    collection = db["Games"]

    passed_slug = request.args.get("slug")

    # Deletes game data by slug from Mongodb
    myCursor = None
    # Query to delete the game by it's slug
    game_query = {"slug": {"$eq": passed_slug}}
    myCursor = collection.delete_one({"$and": [game_query]})
    return "Game has been deleted"
