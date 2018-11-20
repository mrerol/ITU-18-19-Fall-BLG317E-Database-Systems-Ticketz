import psycopg2 as dbapi2
import os
import sys
from .base_dao import BaseDao

class UserDao(BaseDao):
    def __init__(self):
        super(UserDao,self).__init__()

    def add_user(self,user_name, name, surname, gender, email, password, phone, address):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (user_name, name, surname, gender, email, password, phone, address) VALUES (%s, %s,%s, %s,%s, %s,%s, %s) RETURNING user_id",
                (user_name, name, surname, gender, email, password, phone, address)
            )
            userid = cursor.fetchone()
            cursor.close()
        return userid