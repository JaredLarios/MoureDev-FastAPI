from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

import mongoengine as db
from PIL import Image


class User(db.Document):
    name = db.StringField(max_length=40)
    tags = db.ListField(db.ReferenceField("Tag"))
    password = db.StringField(max_length=40)

class Tag(db.Document):
    name = db.StringField(max_length=10)

class FastTag(BaseModel):
    name : str 

class FastUser(BaseModel):
    name : str = Field(max_length=40)
    password : str = Field(max_length=40)
    tags : FastTag

class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.now)
    user = db.ReferenceField(User, required=False)


class Comment(db.EmbeddedDocument):
    name = db.StringField(max_length=20, required=True)
    value = db.StringField(max_length=20)
    tag = db.ReferenceField(Tag)


class Post(db.Document):
    name = db.StringField(max_length=20, required=True)
    value = db.StringField(max_length=20)
    inner = db.ListField(db.EmbeddedDocumentField(Comment))
    lols = db.ListField(db.StringField(max_length=20))


class File(db.Document):
    name = db.StringField(max_length=20)
    data = db.FileField()



class Image(db.Document):
    name = db.StringField(max_length=20)
    image = db.ImageField()


class Video(db.Document):
    name = db.StringField(max_length=20)
    image = db.ReferenceField(Image, required=False)
    print(image)
    data = db.FileField()
    year = db.IntField()



