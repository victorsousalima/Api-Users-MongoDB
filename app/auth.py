from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.parameters import SECRET_KEY, ALGORITHM, EXPIRE
from app.dao.dao_users import select_by_email
from app.dao.dao_auth import verify_token_revoked


oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")

crypt = CryptContext(schemes=["bcrypt"])

def create_token(email: str, name: str):

    payload = {
        "sub" : email,
        "name" : name,
        "exp" : datetime.utcnow() + timedelta(days=EXPIRE),
        "type" : "login"
    }

    try:    
        token = jwt.encode(payload, SECRET_KEY, ALGORITHM)

        return {"access_token" : token}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "token is not created"}
        )


def verify_token(token: str = Depends(oauth)):

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_email = payload["sub"]
        user_exists = select_by_email(user_email)
        token_revoked = verify_token_revoked(token)

        if not user_exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg" : "invalid token"}
            )
        
        if token_revoked:
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


def return_token(token: str = Depends(oauth)):

    token_revoked = verify_token_revoked(token)

    if token_revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"msg" : "invalid token"}
            )

    return token


def hash_password(password: str):

    return crypt.hash(password)


def verify_hash_password(hash_password, password):

    return crypt.verify(password, hash_password)