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
            cursor.execute("SELECT code, city_name FROM city")
            cities = cursor.fetchall()
            cursor.close()
        return cities

    def get_city(self,code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT code, city_name FROM city WHERE (city.code = %s)",(code,))
            city = cursor.fetchone()
            cursor.close()
        return city
    def get_all_cities(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM city")
            cities = cursor.fetchall()
            cursor.close()
        return cities

    def delete_city(self, code):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM city WHERE code = %s", (code,))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def add_city_allCol(self,code,city_name, region, population, altitude):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO city (code, city_name,region, population, altitude) VALUES (%s, %s, %s, %s, %s) ", (code,city_name, region, population, altitude,))
            cursor.close()

    def edit_city(self, code, city_code,city_name, region, population, altitude):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("""UPDATE city SET code = %s, city_name = %s, region = %s, population = %s, altitude = %s WHERE code = %s """, (city_code, city_name, region, population, altitude, str(code),))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def get_city_all(self,code):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM city WHERE (city.code = %s)",(str(code),))
            city = cursor.fetchone()
            cursor.close()
        return city