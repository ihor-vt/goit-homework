import random
from faker import Faker
from src.db import session
from models import Contact, Phone
from time import time


fake = Faker()
fake_phone_ua = Faker('uk_UA')


def create_contacts(count):
    timer = time()
    for _ in range(count):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthday=fake.date_between(start_date='-20y'),
            email=fake.email(),
            address=fake.address())
        session.add(contact)
    session.commit()


def create_phones():
    contacts = session.query(Contact).all()
    for _ in range(len(list(contacts)) + 4):
        contact = random.choice(contacts)
        phones = Phone(cell_phone=fake_phone_ua.phone_number(),
                       contacts_id=contact.id)
        session.add(phones)
    session.commit()


if __name__ == '__main__':
    create_contacts(15)
    create_phones()
