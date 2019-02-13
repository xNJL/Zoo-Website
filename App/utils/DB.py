import pymysql
from pymysql import IntegrityError


class DB:

    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='test',
                                          password='test',
                                          db='fake_db')

    def query(self, sql):
        try:
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
                self.connection.commit()
            except IntegrityError as e:
                return e

        except:
            self.connect()
            cursor = self.connection.cursor()
            try:
                cursor.execute(sql)
                self.connection.commit()
            except IntegrityError as e:
                return e

        return cursor
