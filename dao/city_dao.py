import psycopg2 as dbapi2
import os
import sys
from .base_dao import BaseDao

class CityDao(BaseDao):
    def __init__(self):
        super(CityDao,self).__init__()

    def add_city(self,code,city_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO city (code, city_name) VALUES (%s, %s) ", (code, city_name))
            cursor.close()
    
    def get_city_code(self,city_name):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT code FROM city WHERE (city.city_name = %s)", (city_name,))
            city_code = cursor.fetchone()
            cursor.close()
        return city_code

    def get_all_city(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM city")
            cities = cursor.fetchall()
            cursor.close()
        return cities

    def get_city(self,code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM city WHERE (city.code = %s)",(code,))
            city = cursor.fetchone()
            cursor.close()
        return city