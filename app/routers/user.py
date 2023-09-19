from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.dao import dao_users
from app.schemas.user import User
from app.auth import hash_password, verify_token


router = APIRouter(prefix='/user')

@router.get('/')
def get_all_users():

    users = dao_users.select_all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "No users found!"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get('/email')
def get_by_email(payload: dict = Depends(verify_token)):

    user = dao_users.select_by_email(payload["sub"])

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The user was not found!"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post('/register')
def create_user(user: User):

    user_exists = dao_users.select_by_email(user.email)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"msg": "The user already exists!"})
    
    password_hash = hash_password(user.password)
    user.password = password_hash
    user_created = dao_users.insert(user)

    if not user_created:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The user has not been registered!"})
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "The user has been successfully registered!"})


@router.put('/update')
def update_user(user: User, payload: dict = Depends(verify_token)):

    user_exists = dao_users.select_by_email(payload["sub"])

    if not user_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The user does not exist! "})
    
    password_hash = hash_password(user.password)
    user.password = password_hash
    user_updated = dao_users.update_by_email(payload["sub"], user)

    if not user_updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "The user has not been updated!"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The user has been successfully updated!"})


@router.delete('/delete')
def delete_user(payload: dict = Depends(verify_token)):
    
    user_exists = dao_users.select_by_email(payload["sub"])

    if not user_exists:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The user does not exist! "})
    
    user_deleted = dao_users.delete_by_email(payload["sub"])

    if not user_deleted:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"msg": "The user has not been deleted!"})
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"msg": "The user was successfully deleted!"})