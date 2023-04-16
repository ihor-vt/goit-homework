import sqlite3


def create_db():
    with open('students.sql', 'r') as file:
        sql = file.read()

    with sqlite3.connect('db_students.db') as con:
        cur = con.cursor()
        cur.executescript(sql)


if __name__ == "__main__":
    create_db()
