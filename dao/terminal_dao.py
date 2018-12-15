import psycopg2 as dbapi2
import os
import sys
from .base_dao import BaseDao

class TerminalDao(BaseDao):
    def __init__(self):
        super(TerminalDao,self).__init__()

    def add_terminal(self,terminal_name, terminal_code, email, phone, address, description, city):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO terminal (terminal_name, terminal_code, email, phone, address, description, city_id) VALUES (%s, %s, %s, %s, %s, %s, %s) ", 
                (terminal_name, terminal_code, email, phone, address, description, city))
            cursor.close()
    
    def get_terminal_id(self,terminal_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT terminal_id FROM terminal WHERE (terminal.terminal_name = %s)", (terminal_name,))
            terminal_id = cursor.fetchone()
            cursor.close()
        return terminal_id

    def get_all_terminal(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM terminal JOIN city ON (terminal.city_id = city.code)")
            terminal = cursor.fetchall()
            cursor.close()
        return terminal

    def get_terminal_wname(self,terminal_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM terminal WHERE (terminal.terminal_name = %s)",(terminal_name,))
            terminal = cursor.fetchone()
            cursor.close()
        return terminal
    def get_terminal_wid(self,terminal_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM terminal WHERE (terminal.terminal_id = %s)",(terminal_id,))
            terminal = cursor.fetchone()
            cursor.close()
        return terminal

    def get_all_terminal_city(self,city_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM terminal WHERE terminal.city = %s",(city_name,))
            terminal = cursor.fetchall()
            cursor.close()
        return terminal

    def get_all_terminal_city_wcity_id(self, city_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT terminal_id, terminal_name FROM terminal where city_id = %s ", (city_id,))
            terminal = cursor.fetchall()
            cursor.close()
        return terminal

    def get_all_terminal_v2(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT terminal_name,terminal_code FROM terminal JOIN city ON (terminal.city_id = city.code)")
            terminal = cursor.fetchall()
            cursor.close()
        return terminal