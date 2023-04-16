from mongoengine import *


connect(host='mongodb://localhost:27017/adr-book')


class Contact(Document):
    first_name = StringField(min_length=1, max_length=40, required=True)
    last_name = StringField(min_length=1, max_length=40)
    birthday = DateField()
    email = EmailField(required=True)
    address = StringField(max_length=300)
    phone = ListField(max_length=20, required=True)
    meta = {'indexes': [
        {
         'fields': ['first_name', "$last_name", "$birthday", "$email", "$address", "$phone"],
         'weights': {'first_name': 10, 'last_name': 9, 'birthday': 8, 'email': 7, 'address': 6, 'phone': 5}
        }
    ]}
