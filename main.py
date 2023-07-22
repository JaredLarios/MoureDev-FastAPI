from fastapi import FastAPI, HTTPException, status, Request, Response
from mongoengine import *
from bson import ObjectId
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.mongoengine import Admin, ModelView

from mongoengine import connect, disconnect

from model import File, Image, Post, Todo, User, Video, FastUser, Tag, FastTag

app = FastAPI(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[lambda: connect(
        host="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.1",
        db="local")],
    on_shutdown=[lambda: disconnect()],
)

# Create admin
admin = Admin(title="Example: MongoEngine")


@app.post("/add/")
async def add_user(user: FastUser):
    tag_name = user.tags.name
    if search_user(user.name) == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "User already exist")
    
    user_dict = dict(user)
    tags_ids = search_tag(tag_name)
    user_dict["tags"] = [ObjectId(tags_ids)]
    mongo_item = User(**user_dict).save()
    return({"mesage": "user added", "data": user})

@app.get("/get/")
async def get_tag(tag: str):
    tag_id = search_user(tag)
    return {"message": tag_id}

def search_tag(tag: str):
    tag_dict = Tag.objects(name=tag).get()
    return str(tag_dict.id)

def search_user(user: str):
    try:
        user_dict = User.objects(name=user).get()
        user_dict = user_dict.to_mongo().to_dict()
        print(user_dict)
        if user_dict["name"] != None:
            return True
        
    except:
        return False

def user_scheme(user):
    return {"name": user["name"],
           "password": user["password"],
           "tags": str(user["tags"])
           }


# Add views
class UserView(ModelView):
    fields_default_sort = [(User.name, True)]
    export_fields = [User.id, User.name, User.tags]


admin.add_view(UserView(User, icon="fa fa-users"))
admin.add_view(UserView(Tag, icon="fa fa-users"))
admin.add_view(ModelView(Todo, icon="fa fa-list"))
admin.add_view(ModelView(Post, icon="fa fa-blog", label="Blog Posts"))
admin.add_view(ModelView(File, icon="fa fa-file"))
admin.add_view(ModelView(Video, icon="fa fa-file"))
admin.add_view(ModelView(Image, icon="fa fa-file-image"))

# Mount admin to app
admin.mount_to(app)