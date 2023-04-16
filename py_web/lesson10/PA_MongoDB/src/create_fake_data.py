from PA_MongoDB.src.models import Contact
from faker import Faker


fake = Faker()


def create_contact(count):
    for _ in range(count):
        Contact(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthday=fake.date_between(start_date='-30y'),
            email=fake.ascii_free_email(),
            address=fake.address(),
            phone=sanitize_phone(fake.phone_number())
        ).save()


def sanitize_phone(phone: str):
    edit_phone = phone.strip()\
        .removeprefix('+')\
        .replace('(', '')\
        .replace(')', '')\
        .replace(' ', '')\
        .replace('.', '')\
        .replace('-', '')
    return edit_phone


if __name__ == '__main__':
    create_contact(4)
