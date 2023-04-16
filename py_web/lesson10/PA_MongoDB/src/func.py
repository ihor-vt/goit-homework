from mongoengine import DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset.visitor import Q
from PA_MongoDB.src.models import Contact


class ExceptError:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except DoesNotExist as err:
            print(err)
        except MultipleObjectsReturned as err:
            print(f'Write first name, last name for searching.\nErrors - {err}')
        except Exception as err:
            print(err)


@ExceptError
def bd_create_contact(first_name, last_name, phone):
    Contact(first_name=first_name, last_name=last_name, phone=phone).save()


@ExceptError
def db_change_phone(first_name, last_name, phone):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(phone=phone)


@ExceptError
def bd_delete_phone(first_name, last_name):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(phone='None')


@ExceptError
def bd_update_birthday(first_name, last_name, birthday):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(birthday=birthday)


@ExceptError
def bd_show_birthday(first_name, last_name):
    contact = Contact.objects.get(Q(first_name=first_name) & Q(last_name=last_name))
    birthday = contact.birthday
    return birthday


@ExceptError
def db_show_phone(first_name, last_name):
    contact = Contact.objects.get(Q(first_name=first_name) & Q(last_name=last_name))
    phone = contact.phone
    return phone


@ExceptError
def bd_delete_phone(first_name, last_name):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(phone='None')


@ExceptError
def db_delete_contact(first_name, last_name):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.delete()


@ExceptError
def bd_delete_all():
    Contact.objects.delete()


@ExceptError
def bd_update_email(first_name, last_name, email):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(email=email)


@ExceptError
def bd_update_address(first_name, last_name, address):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name=last_name))
    contact.update(address=address)


@ExceptError
def bd_update_last_name(first_name, last_name):
    contact = Contact.objects(Q(first_name=first_name) & Q(last_name='Incognito'))
    contact.update(last_name=last_name)


@ExceptError
def bd_find_data(sub):
    user = Contact.objects.search_text(sub).first()
    if user:
        return f'\n|{"_" * 90}|\n' \
               f'Name {user.first_name},\n' \
               f'Last name {user.last_name},\n' \
               f'Phone: {user.phone},\n' \
               f'Birthday: {user.birthday},\n' \
               f'Email: {user.email},\n' \
               f'Address: {user.address}' \
               f'\n|{"_" * 90}|\n'
    else:
        return f'Data not found'
