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

    def add_user_with_adminfo(self,user_name, name, surname, gender, email, password, phone, address,is_admin):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (user_name, name, surname, gender, email, password, phone, address, is_admin) VALUES (%s, %s,%s, %s,%s, %s,%s, %s, %s) ",
                (user_name, name, surname, gender, email, password, phone, address, is_admin)
            )
            cursor.close()
    
    def get_user_id(self,user_name,password):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE (users.user_name = %s AND users.password = %s)",
                             (user_name,password)
            )
            userid = cursor.fetchone()
            cursor.close()
        return userid

    def get_user(self,user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE (users.user_id = %s)",(user_id,))
            user = cursor.fetchone()
            cursor.close()
        return user

    def get_all_user(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users ")
            user = cursor.fetchall()
            cursor.close()
        return user

    def delete_user(self, user_id):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def edit_user(self, id,user_name, name, surname, gender, email, password, phone, address, is_admin):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("""UPDATE users SET user_name = %s, email = %s, password = %s, name = %s, surname = %s, gender = %s, address = %s, is_admin = %s WHERE user_id = %s """, (user_name, email, password, name, surname, gender, address,is_admin,id))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_all_user_listing(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, user_name, email, name, surname,is_admin FROM users ")
            user = cursor.fetchall()
            cursor.close()
        return user