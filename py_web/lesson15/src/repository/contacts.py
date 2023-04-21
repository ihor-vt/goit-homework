import datetime
import logging

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactResponse


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(
    db: Session, first_name: str = None, last_name: str = None, email: str = None
):
    if first_name and last_name and email:
        return (
            db.query(Contact)
            .filter(
                Contact.first_name == first_name.capitalize(),
                Contact.last_name == last_name.capitalize(),
                Contact.email == email.lower(),
            )
            .all()
        )
    elif first_name and last_name:
        return (
            db.query(Contact)
            .filter(
                Contact.first_name == first_name.capitalize(),
                Contact.last_name == last_name.capitalize(),
            )
            .all()
        )
    elif last_name and email:
        return (
            db.query(Contact)
            .filter(
                Contact.last_name == last_name.capitalize(),
                Contact.email == email.lower(),
            )
            .all()
        )
    elif first_name and email:
        return (
            db.query(Contact)
            .filter(
                Contact.first_name == first_name.capitalize(),
                Contact.email == email.lower(),
            )
            .all()
        )
    elif first_name:
        return (
            db.query(Contact)
            .filter(Contact.first_name == first_name.capitalize())
            .all()
        )
    elif last_name:
        return (
            db.query(Contact).filter(Contact.last_name == last_name.capitalize()).all()
        )
    elif email:
        return db.query(Contact).filter(Contact.email == email.lower()).all()

    return None


async def birthday_contacts(db: Session):
    # start_day = datetime.date.today() + datetime.timedelta(days=1)
    # end_day = datetime.date.today() + datetime.timedelta(days=8)
    # logging.warning(f"Start_day: {start_day}, End_day: {end_day}")
    # contacts = (
    #     db.query(Contact)
    #     .filter(Contact.birthday >= start_day, Contact.birthday <= end_day)
    #     .all()
    # )
    # logging.warning(f"Found {len(contacts)} contacts")
    # return contacts

    sql_query = """
        SELECT * FROM contact
        WHERE date_part('month', birthday) = date_part('month', CURRENT_DATE + INTERVAL '1 DAY')
            AND date_part('day', birthday) BETWEEN date_part('day', CURRENT_DATE + INTERVAL '1 DAY')
                                            AND date_part('day', CURRENT_DATE + INTERVAL '8 DAY')
    """
    contacts = db.execute(text(sql_query)).fetchall()
    logging.info(f"Found {len(contacts)} contacts")
    return contacts
