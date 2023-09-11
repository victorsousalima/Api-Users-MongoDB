from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from app.parameters import SECRET_KEY, ALGORITHM
from app.dao.dao_users import select_by_email

oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")

crypt = CryptContext(schemes=["bcrypt"])

def create_token(email: str, name: str):

    payload = {
        "sub" : email,
        "name" : name,
        "exp" : datetime.utcnow() + timedelta(days=10),
        "type" : "login"
    }
    
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

    return {"access_token" : token}


def verify_token(token: str = Depends(oauth)):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_email = payload["sub"]
        user_exists = select_by_email(user_email)

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg" : "invalid token"}
            )
        
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "invalid token"}
        )


def hash_password(password: str):

    return crypt.hash(password)


def verify_hash_password(hash_password, password):

    return crypt.verify( password, hash_password)