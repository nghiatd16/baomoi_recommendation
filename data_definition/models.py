from database.models import AbstractModel
from database import fields

class User(AbstractModel):
    username = fields.TextField(allow_none=False)
    password = fields.PasswordField(allow_none=False)
    full_name = fields.TextField(allow_none=True)
    age = fields.IntegerField(allow_none=True)
    gender = fields.BooleanField(allow_none=True)

class News(AbstractModel):
    title = fields.TextField()
    category = fields.TextField()
    body = fields.TextField()
    keywords = fields.ArrayField()
    description = fields.TextField()
    publish_timestamp = fields.IntegerField()

class Clicks(AbstractModel):
    userid = fields.ObjectIdField(allow_none=False)
    newsid = fields.ObjectIdField(allow_none=False)
    timestamp = fields.IntegerField(allow_none=False)
