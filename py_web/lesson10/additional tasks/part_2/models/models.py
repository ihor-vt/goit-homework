from mongoengine import *

from models.db import url

connect(host=url, ssl=True)


class Contacts(Document):
    first_name = StringField(max_length=120, min_length=1, required=True)
    last_name = StringField(max_length=120, min_length=1, required=False)
    age = IntField(min_value=18, max_value=75, required=True)
    email = StringField(required=True)
    cell_phone = StringField(required=True)
    completed_email = BooleanField(default=False)
    completed_sms = BooleanField(default=False)