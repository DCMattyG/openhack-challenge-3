import os
import json
import logging
import pymongo

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rating_id = req.params.get('ratingId')
    
    if rating_id == None:
        return func.HttpResponse(
             "The field 'ratingId' is missing or invalid.",
             status_code=404
        )

    mongo_client = pymongo.MongoClient(os.environ["MONGO_DB_CONN_STR"])
    mydb = mongo_client["openhack"]
    mycol = mydb["ratings"]
    rating = mycol.find_one({ "id": rating_id })

    
    if rating:
        del rating["_id"]

        return func.HttpResponse(
            json.dumps(rating),
                status_code=200,
                mimetype="application/json"
        )
    else:
        return func.HttpResponse(
             f"A rating with the id of {rating_id} does not exist.",
             status_code=404
        )
