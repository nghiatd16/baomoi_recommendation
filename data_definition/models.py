from database.models import AbstractModel
from database import fields


class News(AbstractModel):
    index = fields.TextField()
    title = fields.TextField()
    category = fields.TextField()



