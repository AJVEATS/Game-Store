import pymongo
from pymongo import MongoClient
from bson.json_util import dumps
import os
import requests
import json


def update_mongodb_single_game(request):
    cluster = MongoClient(
        "mongodb+srv://AJVEATS:alexTest@gamestoredb.gaxxodr.mongodb.net/?retryWrites=true&w=majority"
    )
    db = cluster["GameStoreDB"]
    collection = db["Games"]

    slug = request.args.get("oldSlug")
    newSlug = request.args.get("newSlug")
    name = request.args.get("name")
    release = request.args.get("release")
    genre = request.args.get("genre")
    rating = request.args.get("rating")
    ageRating = request.args.get("ageRating")
    image = request.args.get("image")
    price = request.args.get("price")
    description = request.args.get("description")

    myCursor = None
    game_query = {"slug": {"$eq": slug}}
    updated_game = {
        "$set": {
            "slug": newSlug,
            "name": name,
            "released": release,
            "genre": genre,
            "rating": rating,
            "age_rating": ageRating,
            "image": image,
            "price": price,
            "description": description,
        }
    }
    myCursor = collection.update_one(game_query, updated_game)

    return "Game has been updated"
