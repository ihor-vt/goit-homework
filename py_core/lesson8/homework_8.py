
import datetime


def get_birthdays_per_week(users):

    date_today = datetime.datetime.now()

    year_date = date_today.year

    if 'Monday' in date_today.strftime('%A %d %m %Y'):

        days = datetime.timedelta(days=2)

        dif_date = date_today - days

        end_date = (date_today + datetime.timedelta(weeks=1)).timestamp()

        date_today = dif_date.timestamp()

    elif 'Sunday' in date_today.strftime('%A %d %m %Y'):

        days = datetime.timedelta(days=1)

        dif_date = date_today - days

        end_date = (date_today + datetime.timedelta(weeks=1)).timestamp()

        date_today = dif_date.timestamp()

    else:

        end_date = (date_today + datetime.timedelta(weeks=1)).timestamp()

        date_today = dif_date.timestamp()

    for i in range(len(users)):

        for k, v in users[i].items():

            if k == 'birthday':

                value_datetime = datetime.datetime(
                    year=year_date, month=int(v[5:7]), day=int(v[8:]))

                value_timestamp = value_datetime.timestamp()

                if date_today < value_timestamp < end_date:

                    name_week = (value_datetime.strftime(
                        '%A %d %B %Y')).split()

                    weeks_birthday[name_week[0]] = users[i]['name']

    for key, value in weeks_birthday.items():

        if key in ['Saturday', 'Sunday'] and len(value) > 0:

            if len(weeks_birthday['Monday']) > 0:

                weeks_birthday['Monday'].append(value)

                weeks_birthday[key] = []

            else:

                weeks_birthday['Monday'] = value

                weeks_birthday[key] = []

    birthday = ''

    for key, value in weeks_birthday.items():

        if len(value) > 0:

            birthday += f'{key}: {value}\n'

    return birthday


# Тестовий лист
users = [
    {
        "name": "Bill",
        "birthday": "1998-02-08"
    },
    {
        "name": "Giil",
        "birthday": "1999-02-10"
    },
    {
        "name": "Till",
        "birthday": "2000-02-15"
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
