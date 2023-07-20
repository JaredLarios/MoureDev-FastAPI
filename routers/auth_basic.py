from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth",
                   tags=["Authentication"],
                   responses={404: {"message":"not found"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456789"
    },
    "sam11": {
        "username": "sam11", 
        "full_name": "Samuel Larios",
        "email": "example@gmail.com",
        "disabled": False,
        "password": "123456789"
    },
    "sam12": {
        "username": "sam12", 
        "full_name": "Sami Larios",
        "email": "example@gmail.com",
        "disabled": False,
        "password": "123456789"
    },

}


def search_dbuser(username: str):
    if username in users_fake_db: 
        return UserDB(**users_fake_db[username])
    
def search_user(username: str):
    if username in users_fake_db: 
        return Users(**users_fake_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException( 
            status_code=401, detail="unauthorazied", headers={"www-Authenticate": "Bearer"})
    if user.disabled:
            raise HTTPException( 
                status_code=400, detail="user incative", headers={"www-Authenticate": "Bearer"})
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_fake_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    user = search_dbuser(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/user/me")
async def me(user: Users = Depends(current_user)):
    return user
    