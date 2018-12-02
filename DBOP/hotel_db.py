from DBOP.tables.hotel_table import Hotel
from dao.city_dao import CityDao

import psycopg2 as dbapi2
import os


class hotel_database:
    def __init__(self):
        self.hotel = self.Hotel()

    class Hotel:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_hotel(self, hotel):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO hotels ( name, email, description, city, address, phone, website) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website))
                cursor.close()

        def add_hotel_with_logo(self, hotel_with_logo):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO hotels ( name, email, description, city, address, phone, website, logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (hotel_with_logo.name, hotel_with_logo.email, hotel_with_logo.description, hotel_with_logo.city, hotel_with_logo.address, hotel_with_logo.phone, hotel_with_logo.website, hotel_with_logo.logo))
                cursor.close()


        def get_hotel_id(self, hotel):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT hotel_id FROM hotels WHERE name = %s AND email = %s AND description = %s AND city = %s AND address = %s AND phone= %s AND website = %s",
                    (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def delete_hotel(self, hotel_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM hotels WHERE hotel_id = %s", (hotel_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def delete_hotel_logo(self, hotel_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("UPDATE hotels SET logo = NULL WHERE hotel_id = %s", (hotel_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_hotel(self, hotel_id):
            _hotel = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id,))
                hotel = cursor.fetchone()
                if hotel is not None:
                    _hotel = Hotel(hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7], hotel[8])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _hotel

        def get_hotels(self):
            hotels = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM hotels;")
                for hotel in cursor:
                    _hotel = Hotel(hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7], hotel[8])
                    hotels.append((hotel[0], _hotel))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return hotels

        def update_hotel(self, hotel_id, hotel):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE hotels SET name = %s, email = %s, description = %s, city = %s, address = %s, phone = %s, website = %s WHERE hotel_id = %s """, (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website, hotel_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def update_hotel_with_logo(self, hotel_id, hotel):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE hotels SET name = %s, email = %s, description = %s, city = %s, address = %s, phone = %s, website = %s, logo = %s WHERE hotel_id = %s """, (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website, hotel.logo, hotel_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def search(self, text):
            hotels = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM hotels WHERE (name like %s) or (email like %s) or (description like %s) or (address like %s) or (website like %s) or (city like %s)    ;", (to_search, to_search, to_search, to_search, to_search, to_search))
                for hotel in cursor:
                    _hotel = Hotel(hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7], hotel[8])
                    hotels.append((hotel[0], _hotel))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return hotels

        def get_hotels_with_cities(self):
            hotels = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT hotel_id, city_name FROM hotels JOIN city ON hotels.city = city.code;")
                hotels = cursor.fetchall()
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return hotels