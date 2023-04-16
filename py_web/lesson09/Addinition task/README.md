# Друга частина
Замість скрипту seed.py подумайте та реалізуйте повноцінну CLI програму для CRUD операцій із базою даних. Використовуйте для цього модуль argparse .

Використовуйте команду --action або скорочений варіант -a для CRUD операцій. Та команду --model (-m) для вказівки над якою моделлю проводитися операція.

#### Приклад:

* --action create -m Teacher --name 'Boris Jonson' створення вчителя
* --action list -m Teacher показати всіх вчителів
* --action update -m Teacher --id 3 --name 'Andry Bezos' оновити дані вчителя з id=3
* --action remove -m Teacher --id 3 видалити вчителя з id=3
Реалізуйте ці операції для кожної моделі.

# INFO
Приклади виконання команд у терміналі.

**Створити вчителя**

    py main.py -a create -m Teacher -n 'Boris Jonson'

**Створити групу**

    py main.py -a create -m Group -n 'AD-101'  

**Створити студента**

    py main.py -a create -m Student -n 'Name' -gi 1

**Створити дисципліну**

    py main.py -a create -m Discipline -n 'Name' -ti 1

**Створити оцінку**

    py main.py -a create -m Grade -g 10 -d 01.01.1970 -si 1 -di 1


**Оновити вчителя**

    py main.py -a update -m Teacher -n 'Boris Jonson' -i 1

**Оновити групу**

    py main.py -a update -m Group -n 'AD-101' -i 1

...