from fastapi import FastAPI
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
        host="mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh")],
    on_shutdown=[lambda: disconnect()],
)

# Create admin
admin = Admin(title="Example: MongoEngine")

@app.post("/add/")
async def add_user(user: FastUser):
    user_dict = dict(user)
    tags_ids = search_tag(user)
    user_dict["tags"] = []
    mongo_item = User(**user_dict).save()
    return({"mesage": user})

def search_tag(user: FastUser):
    tag_dict = dict(user.tags)
    return ObjectId(tag_dict["tag"])

# Add views
class UserView(ModelView):
    fields_default_sort = [(User.name, True)]


admin.add_view(UserView(User, icon="fa fa-users"))
admin.add_view(UserView(Tag, icon="fa fa-users"))
admin.add_view(ModelView(Todo, icon="fa fa-list"))
admin.add_view(ModelView(Post, icon="fa fa-blog", label="Blog Posts"))
admin.add_view(ModelView(File, icon="fa fa-file"))
admin.add_view(ModelView(Video, icon="fa fa-file"))
admin.add_view(ModelView(Image, icon="fa fa-file-image"))

# Mount admin to app
admin.mount_to(app)