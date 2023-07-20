from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION= 1
SECRET = "5fdc2f322d8159083c1593e15f28a4c99dc86193fb7607fe079c66ee9cf972dd"

router = APIRouter(prefix="/auth2",
                   tags=["Authentication"],
                   responses={404: {"message":"not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class Users(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(Users):
    password: str

users_fake_db = {
    "jedlarios98": {
        "username": "jedlarios98", 
        "full_name": "Jared Larios",
        "email": "example@gmail.com",
        "disabled": False,
        "password": "$2a$12$bZJ4arSfL9sspYKEM64ZSe6PuzA76FMVPz3wNUQmk5D5rlmTA4pOK"
    },
    "sam11": {
        "username": "sam11", 
        "full_name": "Samuel Larios",
        "email": "example@gmail.com",
        "disabled": False,
        "password": "$2a$12$bZJ4arSfL9sspYKEM64ZSe6PuzA76FMVPz3wNUQmk5D5rlmTA4pOK"
    },
    "sam12": {
        "username": "sam12", 
        "full_name": "Sami Larios",
        "email": "example@gmail.com",
        "disabled": False,
        "password": "$2a$12$bZJ4arSfL9sspYKEM64ZSe6PuzA76FMVPz3wNUQmk5D5rlmTA4pOK"
    },
}

def search_dbuser(username: str):
    if username in users_fake_db: 
        return UserDB( **users_fake_db[username] )
    
def search_user(username: str):
    if username in users_fake_db: 
        return Users( **users_fake_db[username] )
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
                        status_code=401, 
                        detail="unauthorazied", 
                        headers={"www-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

        return search_user(username)
    
    except JWTError:
        raise exception


    
async def current_user(user: Users = Depends(auth_user)):
    if user.disabled:
            raise HTTPException( 
                status_code=400, detail="user incative", headers={"www-Authenticate": "Bearer"})
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    #user_db = users_fake_db.get(form.username)
    #if not user_db:
    #    raise HTTPException(
    #        status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_dbuser(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    access_token = {"sub":user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/user/me")
async def me(user: Users = Depends(current_user)):
    return user