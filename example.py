#fast api
from fastapi import FastAPI, status, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional, Union
from pydantic import BaseModel

# delete auth_basic, products, jwt_auth
# from app.routers import auth_basic, products, jwt_auth, myplus
from routers import auth_basic, products, jwt_auth, myplus



app = FastAPI()

# routers
app.include_router(myplus.router)
app.include_router(products.router)
app.include_router(auth_basic.router)
app.include_router(jwt_auth.router)

class User(BaseModel):
    id: int 
    name : str
    surname : str
    email : str
    url : str
    age : int

users_fake_db = [User(id=1, name="Rossell", surname="Nicoleson", email="ross.example@gmail.net", url="https://jaredlarios.github.com/my-profile", age=25),
                User(id=2, name="Jed", surname="Larios", email="example@lairos.com", url="https://jaredlarios.github.com/my-profile", age=15),
                User(id=3, name="Erwin", surname="Larios", email="example.erwin@lairos.com", url="https://erwin.github.com/my-profile", age=20),
                User(id=4, name="Sam", surname="Larios", email="example.sam@lairos.com", url="https://sam.github.com/my-profile", age=30)]

@app.get("/users/")
async def users():
    return users_fake_db

# GET for path
@app.get("/user/{id}")
async def user(id: int):
    if search_user(id):
        return search_user(id)
    else:
        raise HTTPException(status_code=404, detail= "user not found")

# GET for query
@app.get("/userquery/")
async def user(id: int):
    if search_user(id):
        return search_user(id)
    else:
        raise HTTPException(status_code=404, detail= "user not found")

# POST (add) user
@app.post("/user/", status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail= "user already exist")
        
    else:
        users_fake_db.append(user)
        return user

# PUT (update) user
@app.put("/user/")
async def user(user: User):
    found = False
    for index, save_user in enumerate(users_fake_db):
        if save_user.id == user.id:
            users_fake_db[index] = user
            found = True

    if not found:
        raise HTTPException(status_code=404, detail= "user not found")
    else:
        return user
    
# DELETE a user
@app.delete("/user/{id}", status_code=202)
async def user(id: int):
    found = False
    for index, save_user in enumerate(users_fake_db):
        if save_user.id == id:
            del users_fake_db[index]
            found = True
    if not found:
        raise HTTPException(status_code=404, detail= "user not found")
    else:
        return {"message": "user deleted"}


# serach function 
def search_user(id: int):
    try:
        list_user = filter(lambda user:  user.id == id, users_fake_db)
        return list(list_user)[0]
    except:
        return False
