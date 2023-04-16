import datetime

def get_birthdays_per_week(users):

    date_now = datetime.datetime.now()
    
    date_now_str = date_now.strftime("%Y %m %d").split()
    
    # Обнуляю час на 0
    date_today = datetime.datetime(year = int(date_now_str[0]), month = int(date_now_str[1]), day = int(date_now_str[2]))

    year_date = date_today.year

    start_date = date_today 

    while 'Saturday' not in start_date.strftime('%A %d %m %Y'):
        
        start_date = start_date + datetime.timedelta(days=1)

    if 'Saturday' in start_date.strftime('%A %d %m %Y') and start_date.timestamp() >= date_today.timestamp():

        stop_date_plus = start_date + datetime.timedelta(days=6)

        stop_date = stop_date_plus.timestamp() #Визначили timestamp кiнця нового тижня П`ятниця
        
        start_date = start_date.timestamp() #Визначили timestamp початок вiдрахування Субота

        for i in range(len(users)):

            for k, v in users[i].items():

                if k == 'birthday':

                    value_datetime = datetime.datetime(
                        year=year_date, month=int(v[5:7]), day=int(v[8:]))

                    value_timestamp = value_datetime.timestamp() #Визначили timestamp Дня Народження працiвника

                    if start_date <= value_timestamp <= stop_date:

                        name_week = (value_datetime.strftime(
                            '%A %d %B %Y')).split()

                        weeks_birthday[name_week[0]].append(users[i]['name'])

        for key, value in weeks_birthday.items():

            if key in ['Saturday', 'Sunday'] and len(value) > 0:
                    
                    weeks_birthday['Monday'].append(value)

                    weeks_birthday[key] = []

        birthday = ''

        for key, value in weeks_birthday.items():

            if len(value) > 0:

                birthday += f'{key}: {value}\n'

        return birthday

# Тестовий лист
users = [
    {
        "name": "Bill!!",
        "birthday": "1998-02-13"
    }
]

weeks_birthday = {
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': [],
    'Saturday': [],
    'Sunday': []
}

print(get_birthdays_per_week(users))
