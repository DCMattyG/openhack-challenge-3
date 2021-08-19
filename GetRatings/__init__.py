import os
import json
import logging
import pymongo

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    user_id = req.params.get('userId')
    
    if user_id == None:
        return func.HttpResponse(
             "The field 'userId' is missing or invalid.",
             status_code=404
        )

    mongo_client = pymongo.MongoClient(os.environ["MONGO_DB_CONN_STR"])
    mydb = mongo_client["openhack"]
    mycol = mydb["ratings"]
    ratings = list(mycol.find({ "userId": user_id }))
    
    if len(ratings) != 0:
        for rating in ratings:
            del rating["_id"]

        return func.HttpResponse(
            json.dumps(ratings),
                status_code=200,
                mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             f"No ratings found for the userId of {user_id}.",
             status_code=404
        )
