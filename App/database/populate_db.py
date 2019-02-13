from datetime import datetime as dt

import pandas as pd
import pymysql

# from database_project.App.model.User import User
from App.model.User import User


def populate_animal(c):
    sql = (
        "INSERT INTO fake_db.ANIMAL (NAME, SPECIES, TYPE, AGE, EXHIBIT) "
        "VALUES (%s, %s, %s, %s, %s)"
    )

    df_animal = pd.read_csv('Animal.csv', sep=',', header=None)

    data = []

    for _, row in df_animal.iterrows():
        age = row[3].split()[0]

        data.append([row[0], row[1], row[2], age, row[4]])

    c.executemany(sql, data)


def populate_exhibit(c):
    sql = (
        "INSERT INTO fake_db.EXHIBIT (NAME, WATER, SIZE) "
        "VALUES (%s, %s, %s)"
    )

    df_exhibit = pd.read_csv('Exhibit.csv', sep=',', header=None)

    data = []

    for _, row in df_exhibit.iterrows():
        name, water, size = row

        water = 1 if water == 'Yes' else 0

        data.append([name, water, size])

    c.executemany(sql, data)


def populate_user(c):
    sql = (
        "INSERT INTO fake_db.USER (USERNAME, EMAIL, TYPE, PASSWORD_HASH) "
        "VALUES (%s, %s, %s, %s)"
    )

    df_user = pd.read_csv('User.csv', sep=',', header=None)

    data = []

    for _, row in df_user.iterrows():
        username, password, email, type = row

        type = type.upper()

        user = User(username=username, email=email, user_type=type)
        user.set_password(password)

        data.append([user.username, user.email, user.user_type, user.password_hash])

    c.executemany(sql, data)


def populate_visitor(c):
    sql = (
        "INSERT INTO fake_db.VISITOR (USERNAME) "
        "VALUES (%s)"
    )

    df_user = pd.read_csv('User.csv', sep=',', header=None)

    df_user = df_user[df_user[3] == 'visitor']

    data = []

    for _, row in df_user.iterrows():
        username, _, _, _ = row

        data.append([username])

    c.executemany(sql, data)


def populate_staff(c):
    sql = (
        "INSERT INTO fake_db.STAFF (USERNAME) "
        "VALUES (%s)"
    )

    df_user = pd.read_csv('User.csv', sep=',', header=None)

    df_user = df_user[df_user[3] == 'staff']

    data = []

    for _, row in df_user.iterrows():
        username, _, _, _ = row

        data.append([username])

    c.executemany(sql, data)


def populate_admin(c):
    sql = (
        "INSERT INTO fake_db.ADMIN (USERNAME) "
        "VALUES (%s)"
    )

    df_user = pd.read_csv('User.csv', sep=',', header=None)

    df_user = df_user[df_user[3] == 'admin']

    data = []

    for _, row in df_user.iterrows():
        username, _, _, _ = row

        data.append([username])

    c.executemany(sql, data)


def populate_show(c):
    sql = (
        "INSERT INTO fake_db.SHOW (NAME, DATE_TIME, HOST, EXHIBIT) "
        "VALUES (%s, %s, %s, %s)"
    )

    df_show = pd.read_csv('Show.csv', sep=',', header=None)

    data = []

    for _, row in df_show.iterrows():
        name, date_time, host, exhibit = row

        date_time = dt.strptime(date_time, '%m/%d/%y %I:%M%p')

        data.append([name, date_time, host, exhibit])

    c.executemany(sql, data)


if __name__ == "__main__":
    connection = pymysql.connect(host='localhost',
                                 user='test',
                                 password='test',
                                 autocommit=True)

    cursor = connection.cursor()

    populate_exhibit(cursor)
    populate_animal(cursor)
    populate_user(cursor)
    populate_visitor(cursor)
    populate_staff(cursor)
    populate_admin(cursor)
    populate_show(cursor)

    cursor.close()
    connection.close()
