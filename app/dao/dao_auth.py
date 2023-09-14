from jose import jwt
from datetime import datetime

from pymongo import MongoClient
from app.parameters import HOST, DB
from app.parameters import SECRET_KEY, ALGORITHM

def connect_mongo():

    try:
        client = MongoClient(HOST)
        mydb = client[DB]
        collection = mydb["revoked_token"]
    
    except Exception as error:
        raise Exception('Error when connecting to the database!')
    
    else:
        return client, collection


def saving_token_logout(token: str):

    client, collection = connect_mongo()

    payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)

    saving = {"token": token, "expired": datetime.fromtimestamp(payload["exp"])}

    try:
        collection.insert_one(saving)
    
    except Exception as error:
        client.close()

        return False
    
    else:
        client.close()

        return True


def verify_token_revoked(token: str):

    client, collection = connect_mongo()

    filter = {"token" : token}

    try:
        token_exists = collection.find_one(filter)
    
    except Exception as error:
        client.close()

        return False
    
    else:
        client.close()

        return bool(token_exists)