contacts = {}
continuation_of_work = False


def input_error(func):
    def inner(*args, **kwargs):
        result = False
        try:
            result = func(*args, **kwargs)
        except TypeError:
            print("Give me name and phone please")
        except ValueError:
            print("Wrong command entered.")
        except KeyError:
            print("This name is not in list.")
        return result

    return inner


@input_error
def adder(name, number):
    if name in contacts.keys():
        return False
    contacts[name] = number


@input_error
def changer(name, number):
    if name not in contacts.keys():
        raise KeyError
    contacts[name] = number


@input_error
def print_phone(name):
    number = contacts[name]
    if number:
        print(number)


def print_contacts():
    correct_str = ''
    for name, number in contacts.items():
        correct_str += f"{name}: {number}\n"
    return correct_str


def goodbye():
    print("Goodbye!")
    exit()


commands = {
    'hello': lambda: print("How can I help you?"),
    "add": adder,
    "change": changer,
    "phone": print_phone,
    "show all": lambda: print(print_contacts()),
    '.': goodbye,
    'goodbye': goodbye,
    'close': goodbye,
    'exit': goodbye
}


def parser(command):
    global continuation_of_work
    for key in commands.keys():
        if command.startswith(key):
            new_line = command[len(key):].title()
            commands[key](*new_line.split())
            continuation_of_work = True
            break


@input_error
def main():
    global continuation_of_work
    while True:
        input_commands = input('Введіть команду: ').lower().strip()
        parser(input_commands)
        if not continuation_of_work:
            raise ValueError


if __name__ == '__main__':
    while not continuation_of_work:
        main()
