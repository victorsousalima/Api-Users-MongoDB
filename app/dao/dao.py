from pymongo import MongoClient
from app.parameters import HOST, DB, COLLECTION


def connect_mongo():

    try:
        client = MongoClient(HOST)
        mydb = client[DB]
        collection = mydb[COLLECTION]
    
    except Exception as error:
        raise Exception('Error when connecting to the database!')
    
    else:
        return client, collection
