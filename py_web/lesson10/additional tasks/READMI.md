***Домашнє завдання***

**Перша частина**

Вихідні дані
У нас є json файл з авторами та їх властивостями: дата та місце народження, короткий опис біографії.

[
  {
    "fullname": "Albert Einstein",
    "born_date": "March 14, 1879",
    "born_location": "in Ulm, Germany",
    "description": "In 1879, Albert Einstein was born in ..."
  },
  {
    "fullname": "Steve Martin",
    "born_date": "August 14, 1945",
    "born_location": "in Waco, Texas, The United States",
    "description": "Stephen Glenn \"Steve\" Martin is an American actor, ..."
  }
]

Також ми маємо наступний json файл із цитатами від цих авторів.

[
  {
    "tags": [
      "change",
      "deep-thoughts",
      "thinking",
      "world"
    ],
    "author": "Albert Einstein",
    "quote": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”"
  },
  {
    "tags": [
      "inspirational",
      "life",
      "live",
      "miracle",
      "miracles"
    ],
    "author": "Albert Einstein",
    "quote": "“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”"
  },
  {
    "tags": [
      "adulthood",
      "success",
      "value"
    ],
    "author": "Albert Einstein",
    "quote": "“Try not to become a man of success. Rather become a man of value.”"
  },
  {
    "tags": [
      "humor",
      "obvious",
      "simile"
    ],
    "author": "Steve Martin",
    "quote": "“A day without sunshine is like, you know, night.”"
  }
]

Порядок виконання
1. Створіть хмарну базу даних Atlas MongoDB
2. За допомогою ODM Mongoengine створіть моделі для зберігання даних із цих файлів у колекціях authors та quotes.
3. Під час зберігання цитат (quotes), поле автора в документі повинно бути не рядковим значенням, а Reference fields полем, де зберігається ObjectID з колекції authors.
4. Напишіть скрипти для завантаження json файлів у хмарну базу даних.
5. Реалізуйте скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів. Скрипт виконується в нескінченному циклі і за допомогою звичайного оператора input приймає команди у наступному форматі команда: значення. Приклад:
- name: Steve Martin — знайти та повернути список всіх цитат автора Steve Martin;
- tag:life — знайти та повернути список цитат для тега life;
- tags:life,live — знайти та повернути список цитат, де є теги life або live (примітка: без пробілів між тегами life, live);
- exit — завершити виконання скрипту;
6. Виведення результатів пошуку лише у форматі utf-8;

**Додаткове завдання**
1. Подумайте та реалізуйте для команд name:Steve Martin та tag:life можливість скороченого запису значень для пошуку, як name:st та tag:li відповідно;
2. Виконайте кешування результату виконання команд name: та tag: за допомогою Redis, щоб при повторному запиті результат пошуку брався не з MongoDB бази даних, а з кешу;

**Друга частина**

Напишіть два скрипти: consumer.py та producer.py. Використовуючи RabbitMQ, організуйте за допомогою черг імітацію розсилки email контактам.

Використовуючи ODM Mongoengine, створіть модель для контакту. Модель обов'язково повинна включати поля: повне ім'я, email та логічне поле, яке має значення False за замовчуванням. Воно означає, що повідомлення контакту не надіслано і має стати True, коли буде відправлено. Інші поля для інформаційного навантаження можете придумати самі.

Під час запуску скрипта producer.py він генерує певну кількість фейкових контактів та записує їх у базу даних. Потім поміщає у чергу RabbitMQ повідомлення, яке містить ObjectID створеного контакту, і так для всіх згенерованих контактів.

Скрипт consumer.py отримує з черги RabbitMQ повідомлення, обробляє його та імітує функцією-заглушкою надсилання повідомлення по email. Після надсилання повідомлення необхідно логічне поле для контакту встановити в True. Скрипт працює постійно в очікуванні повідомлень з RabbitMQ.

**Додаткове завдання**

Введіть у моделі додаткове поле телефонний номер. Також додайте поле, що відповідає за кращий спосіб надсилання повідомлень — SMS по телефону або email. Нехай producer.py відправляє у різні черги контакти для SMS та email. Створіть два скрипти consumer_sms.py та consumer_email.py, кожен з яких отримує свої контакти та обробляє їх.