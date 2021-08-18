import os
import logging
from pymongo.message import delete
import requests
import uuid
import json
import pymongo
from datetime import datetime

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass

    if userId:
        mongo_client = pymongo.MongoClient(os.environ["MONGO_DB_CONN_STR"])
        mydb = mongo_client["openhack"]
        mycol = mydb["ratings"]
        ratings = list(mycol.find({ "userId" : userId}))
        for rating in ratings:
            del rating["_id"]
        return func.HttpResponse(json.dumps(ratings),
             status_code=200,
             mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
