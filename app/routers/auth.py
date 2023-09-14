from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.dao import dao_users
from app.dao.dao_auth import saving_token_logout
from app.utils import verify_hash_password, create_token, verify_token, return_token

router = APIRouter(
    prefix="/auth",
    tags=["Autentication"]
)


@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):

    user_exist = dao_users.select_by_email(user.username)

    if not user_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"msg": "User not exists"})
    
    check_password_hash = verify_hash_password(user_exist["password"], user.password)

    if check_password_hash:
        token = create_token(user.username, user_exist["name"])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=token
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "login or password error"}
        )


@router.post("/logout")
def logout(token: str = Depends(return_token)):

    token_revoked = saving_token_logout(token)

    if not token_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"msg": "error revoking token"}
        )
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"msg": "The token is revoked!"})



@router.get("/")
def token_check(token: str = Depends(verify_token)):

    if token["type"] == 'login':
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"msg": "Token is valid", "type": "login"}
            )