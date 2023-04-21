from faker import Faker
from src.database.db import DBSession
from src.database.models import Contact


fake = Faker()
session = DBSession()
DEFAULT_CONTACTS = 100


def create_contact_person(quantity):
    for _ in range(quantity):
        contact = Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.ascii_free_email(),
            phone_number=fake.phone_number(),
            birthday=fake.date_of_birth(),
            description=fake.text(),
        )
        session.add(contact)
    session.commit()


if __name__ == "__main__":
    create_contact_person(DEFAULT_CONTACTS)
