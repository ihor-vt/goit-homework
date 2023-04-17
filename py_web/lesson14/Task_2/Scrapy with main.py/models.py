from mongoengine import *

from db import url


connect_to_db = connect(host=url, ssl=True)


class Authors(Document):
    fullname = StringField(required=True, max_length=250)
    born_date = StringField(max_length=250)
    born_location = StringField(max_length=250)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=250, required=True))
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()