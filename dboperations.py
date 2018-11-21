from tables import Hotel
import psycopg2 as dbapi2
import os
import sys

class Database:
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

        def get_hotel(self, hotel_id):
            _hotel = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM hotels WHERE hotel_id = %s", (hotel_id,))
                hotel = cursor.fetchone()
                if hotel is not None:
                    _hotel = Hotel(hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7])
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
                    _hotel = Hotel(hotel[1], hotel[2], hotel[3], hotel[4], hotel[5], hotel[6], hotel[7])
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
                statement = """UPDATE hotels SET name = '""" + hotel.name + """' , email = '""" + hotel.email +"""' , description = '""" + hotel.description + """', city = ' """ + hotel.city +"""' ,  address = '""" + hotel.address + """', phone = '""" + hotel.phone +"""', website = '""" + hotel.website + """'   WHERE hotel_id = """ + str(hotel_id)
                print(statement)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()