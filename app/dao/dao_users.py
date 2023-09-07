from app.dao.dao import connect_mongo
from app.schemas.user import User

def select_all():

    client, collection = connect_mongo()

    users = []

    try:
        for user in collection.find({}, {"_id" : 0, "name": 1, "email": 1, "cpf": 1, "password": 1}):
            users.append(user)
        
    except Exception as error:
        client.close()

        return None
    
    else:
        client.close()

        return users


def insert(user: User):

    client, collection = connect_mongo()

    try:
        collection.insert_one(dict(user))

    except Exception as error:
        client.close()

        return False
    
    else:
        client.close()

        return True
    

def select_by_email(email: str):

    client, collection = connect_mongo()

    filter = {'email': email}

    try:
        user = collection.find_one(filter, {"_id" : 0, "name": 1, "email": 1, "cpf": 1, "password": 1})

    except Exception as error:
        client.close()

        return None
    
    else:
        client.close()

        return user


def update_by_email(email: str, user: User):

    client, collection = connect_mongo()

    filter = {'email': email}
    new_values = {"$set": {'name': user.name, 'email': user.email, 'cpf': user.cpf, 'password': user.password}}

    try:
        collection.update_one(filter, new_values)
    
    except Exception as error:
        client.close()

        return False
    
    else:
        client.close()

        return True
    

def delete_by_email(email: str):

    client, collection = connect_mongo()

    filter = {'email': email}

    try:
        collection.delete_one(filter)
    
    except Exception as error:
        client.close()

        return False
    
    else:
        client.close()

        return True