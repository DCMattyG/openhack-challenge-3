import os
import logging
from pymongo.message import delete
import requests
import uuid
import json
import pymongo
from datetime import datetime

import azure.functions as func

SAMPLE_DATA = [
    {
        "id": "79c2779e-dd2e-43e8-803d-ecbebed8972c",
        "userId": "cc20a6fb-a91f-4192-874d-132493685376",
        "productId": "4c25613a-a3c2-4ef3-8e02-9c335eb23204",
        "timestamp": "2018-05-21 21:27:47Z",
        "locationName": "Sample ice cream shop",
        "rating": 5,
        "userNotes": "I love the subtle notes of orange in this ice cream!"
    },
    {
        "id": "79c2779e-dd2e-43e8-803c-ecbebed8972c",
        "userId": "cc20a6fb-a91f-4192-874d-132493685376",
        "productId": "4c25613a-a3c2-4ef3-8e02-9c335eb23204",
        "timestamp": "2018-05-21 21:27:47Z",
        "locationName": "Sample ice cream shop",
        "rating": 4,
        "userNotes": "I love the subtle notes of orange in this ice cream!"
    },
    {
        "id": "79c2779e-dd2e-43e8-803a-ecbebed8972c",
        "userId": "cc20a6fb-a91f-4192-874d-132493685376",
        "productId": "4c25613a-a3c2-4ef3-8e02-9c335eb23204",
        "timestamp": "2018-05-21 21:27:47Z",
        "locationName": "Sample ice cream shop",
        "rating": 3,
        "userNotes": "I love the subtle notes of orange in this ice cream!"
    }
]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ratingId = req.params.get('ratingId')
    if not ratingId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass

    if ratingId:
        mongo_client = pymongo.MongoClient(os.environ["MONGO_DB_CONN_STR"])
        mydb = mongo_client["openhack"]
        mycol = mydb["ratings"]
        rating = mycol.find_one({ "id" : ratingId})
        del rating["_id"]
        return func.HttpResponse(json.dumps(rating),
             status_code=200,
             mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
