import psycopg2 as dbapi2
import os
import sys
from .base_dao import BaseDao

class UserDao(BaseDao):
    def __init__(self):
        super(UserDao,self).__init__()

    def add_user(self,username,password):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id",
                (username, password)
            )
            userid = cursor.fetchone()
            cursor.close()
        return userid
