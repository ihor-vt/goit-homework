import datetime
import re
from datetime import date
import phonenumbers
from abc import ABC, abstractmethod
from PA_MongoDB.src.func import *


class Field(ABC):
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self):
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @abstractmethod
    def value(self):
        ...


class FirstName(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class LastName(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            number = phonenumbers.parse(value, "ITU-T")
            self.__value = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            print("Enter correct number, for example +380674444333")
            raise ValueError


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return 'Unknown'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                print("Enter the date of birth (dd.mm.yyyy)")


class Address(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        result = None
        get_email = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
        for i in get_email:
            result = i
        if result is None:
            raise AttributeError(f" Email is not correct {value}")
        self.__value = result


class Record:
    def __init__(self, first_name=None, last_name=None, phones=None, birthday=None, email=None, address=None) -> None:
        if phones is None:
            phones = []
        self.first_name = first_name
        self.last_name = last_name
        self.phone_list = phones
        self.birthday = birthday
        self.address = address
        self.email = email

    def __str__(self) -> str:
        return f'\n|{"_" * 90}|\n' \
               f' Contact:  {self.first_name.value.title()} {self.last_name.value}\n' \
               f' Phones:   {", ".join([phone.value for phone in self.phone_list])}\n' \
               f' Birthday: {self.birthday}\n' \
               f' Email:    {self.email}\n' \
               f' Address:  {self.address}' \
               f'\n|{"_" * 90}|\n'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)

    @staticmethod
    def days_to_birthday(self, birthday: Birthday):
        if birthday.value is None:
            return None
        this_day = date.today()
        birthday_day = date(this_day.year, birthday.value.month, birthday.value.day)
        if birthday_day < this_day:
            birthday_day = date(this_day.year + 1, birthday.value.month, birthday.value.day)
        return (birthday_day - this_day).days


class InputError:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Error! Print correct data!'
        except KeyError:
            return 'Error! User not found!'
        except ValueError:
            return 'Error! Data is incorrect!'
        except AttributeError:
            return "Enter correct the date of birth (dd.mm.yyyy) for this user"


def greeting(*args):
    return 'Hello! How can I help you?'


@InputError
def add_contact(*args):
    first_name = FirstName(*args[0])
    if len(args) == 3:
        last_name = LastName(args[1])
        phone = Phone(args[2])
    elif len(args) == 2:
        last_name = LastName('Incognito')
        phone = Phone(args[1])
    bd_create_contact(first_name.value, last_name.value, phone.value)
    return f'Add user {first_name.value.title()} {last_name.value.title()} with phone number: {phone}'


@InputError
def change_contact(*args):
    first_name, last_name, new_phone = args[0], args[1], args[2]
    db_change_phone(first_name, last_name, new_phone)
    return f'Change phone number {new_phone} to user {first_name} {last_name}'


@InputError
def show_all(*args):
    num_users = Contact.objects.count()
    pag = '-' * 70
    print(f'{pag}\nContacts: {num_users}\nContact list\n{pag}')
    for c in Contact.objects:
        print(
            f'Name: {c.first_name} \n'
            f'Last name: {c.last_name} \n'
            f'Phone: {c.phone}\n'
            f'Email: {c.email}\n'
            f'Birthday: {c.birthday}\n'
            f'Address: {c.address}\n'
            f'{pag}')
    return 'The operation was successful'


@InputError
def del_phone(*args):
    first_name, last_name = args[0], args[1]
    bd_delete_phone(first_name, last_name)
    return f'Delete phone from user {first_name} {last_name}'


@InputError
def add_birthday(*args):
    first_name, last_name, birthday = args[0], args[1], args[2]
    bd_update_birthday(first_name, last_name, birthday)
    return f'Add/modify birthday {birthday} to user {first_name} {last_name}'


@InputError
def user_birthday(*args):
    first_name = args[0]
    last_name = args[1]
    birthday = bd_show_birthday(first_name, last_name)
    if not birthday:
        return 'User has no birthday'
    else:
        return f'Birthday {first_name} {last_name} in: {birthday}'


@InputError
def show_phone(*args):
    first_name = args[0]
    last_name = args[1]
    phones = db_show_phone(first_name, last_name)
    if phones:
        return f'Contact {first_name} {last_name} have phone {phones}'
    else:
        return f'Contact {first_name} {last_name} not found!'


@InputError
def del_user(*args):
    first_name = args[0]
    last_name = args[1]
    confirmation = input(f'Are you sure you want to delete the user {first_name}? (Y/n) >>> ').strip().lower()
    if confirmation == 'y':
        db_delete_contact(first_name, last_name)
        return f'Delete user {first_name} {last_name}'

    else:
        return 'User not deleted'


@InputError
def clear_all(*args):
    confirmation = input('Are you sure you want to delete all users? (Y/n) >>> ').strip().lower()
    if confirmation == 'y':
        bd_delete_all()
        return 'Address book is empty'
    else:
        return 'Removal canceled'


@InputError
def add_email(*args):
    first_name, last_name, email = args[0], args[1], args[2]
    bd_update_email(first_name, last_name, email)
    return f'Add/modify email {email} to user {first_name} {last_name}'


@InputError
def add_address(*args):
    first_name, last_name, address = args[0], args[1], list(args[2:])
    address = " ".join(address)
    bd_update_address(first_name, last_name, address)
    return f'Add/modify address {address.title()} to user {first_name} {last_name}'


@InputError
def add_last_name(*args):
    first_name, last_name = args[0], args[1]
    bd_update_last_name(first_name, last_name)
    return f'Add/modify last name {last_name} to user {first_name}'


@InputError
def find(*args):
    sub = ' '.join(args)
    data = bd_find_data(sub)
    return data


def info():
    return """
    *********** Service command ***********
    "help", "?"                                 --> Commands list
    "close", "exit", "."                        --> Exit from AddressBook

    *********** Add/edit command **********
    "add" first name last name  phone           --> Add user to AddressBook
    "change" first name last name  new_phone    --> Change the user's phone number
    "birthday" first name last name birthday    --> Add/edit user birthday
    "email" first name last name email          --> Add/edit user email
    "last name" first name last name            --> Add/edit user last name
    "address" first name last name address      --> Add/edit user address

    *********** Delete command ***********
    "del" first name last name                  --> Delete phone number
    "delete" first name last name               --> Delete user
    "clear"                                     --> Delete all users

    *********** Info command *************
    "show" first name last name                 --> Show user info
    "show all"                                  --> Show all users info
    "user birthday" first name last name        --> Show how many days to user birthday
    "find" data                                 --> Find any data 
    """


def exiting():
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


COMMANDS = {greeting: ['hello'],
            add_contact: ['add '],
            change_contact: ['change '],
            info: ['help', '?'],
            show_all: ['show all'],
            exiting: ['good bye', 'close', 'exit', '.'],
            del_phone: ['del '],
            add_birthday: ['birthday'],
            user_birthday: ['user birthday '],
            show_phone: ['show '],
            del_user: ['delete '],
            clear_all: ['clear'],
            add_email: ['email '],
            add_address: ['address'],
            add_last_name: ['last name'],
            find: ['find']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    print(info())
    while True:
        user_command = input('Enter your command: >>> ')
        if user_command == 'exit':
            return 'Good bye!'
        command, data = command_parser(user_command)
        print(command(*data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()
