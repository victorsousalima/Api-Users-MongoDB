from pymongo import MongoClient
from app.parameters import HOST, PORT, DB, COLLECTION


def connect_mongo():

    try:
        client = MongoClient(host = HOST, port = PORT)
        mydb = client[DB]
        collection = mydb[COLLECTION]
    
    except Exception as error:
        client.close()
        raise Exception('Error when connecting to the database!')
    
    else:
        return client, collection
