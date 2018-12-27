Parts Implemented by Abdullah AKGÜL
===================================

In this section, there are three main tables which are
hotels, expeditions and tickets table, also there two
extra tables which are images and seats table.
The responsibility of these tables belongs to Abdullah AKGÜL.
Attributes of tables which are mentioned above can be seen
in Figure 1.


.. figure:: images/member3/figure1.png
     :scale: 75 %
     :alt: Abdullah AKGÜL's tables

     Figure 1 - Tables that implemented by Abdullah AKGÜL

Hotels Table
------------

Hotels table is created for recommending users proper hotels. Hotels table is used for store the information about hotels.
The attributes of hotel tables are hotel_id, name, email,
description, city, address, phone, website, logo.
hotel_id is primary key for hotels table. there is one more key attribute
that is city. city attribute is foreign key and the reference of the
city attribute is code attribute of the city table.





.. figure:: images/member3/figure1.png
     :scale: 75 %
     :alt: Hotel table

     Figure 1 - Hotel table

Creation of hotels table and types of attributes of hotels table are given below;

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS hotels
    (
        hotel_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (25) NOT NULL,
        email VARCHAR (50) NOT NULL,
        description VARCHAR (250) NOT NULL,
        city VARCHAR(2),
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        website VARCHAR (50),
        logo BYTEA,
        FOREIGN KEY (city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE

    )

Only users that are admin can manipulate the hotels table.

Operations
^^^^^^^^^^

Operations on the hotels table is handled with hotel
class that is given below.

.. code-block:: python

    class Hotel:
        def __init__(self, name, email, description, city, address, phone, website, logo = None):
            self.name = name
            self.email = email
            self.description = description
            self.city = city
            self.address = address
            self.phone = phone
            self.website = website
            self.logo = logo

This class corresponds the hotel table in the database.
The attributes are same with hotel table.
This class provides ease on operations on the hotels table.


The operations on the hotels table are handled with given below class.
With this class database connection is provided and operations are handled with
functions of this class

.. code-block:: python

    class Hotel:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")




Operations on the hotels table is listed below.



INSERT
______

Insertion of hotel on hotels table can be performed with two ways.
The one of inserting is inserting hotel without logo attribute.
With this way, logo attribute will be NULL.
Related function is given below as add_hotel_with_logo.
Other way is inserting hotel with logo attribute.
The data for logo is provided with given below code.

.. code-block:: python

    logo = request.files["logo"].read()

These functions takes hotel parameter which is hotel class.

.. code-block:: python

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

With this insertion functions new hotel will be added as a row to hotels table.

Read
____

There are three different methods for reading data from
hotels table. These methods are given below.


.. code-block:: python

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


get_hotel method takes hotel_id as parameter. This method
simply returns desired hotel as hotel class.

get_hotels method is used for returns whole hotels in hotels table.
This methods returns an array that created with tuple
which is hotel_id, hotel as hotel class.

get_hotels_with_cities method is nearly same with get_hotels.
The difference is that get_hotels_with_cities returns whole hotels
in the hotels table with city names by using JOIN with city table.

The logo of the hotel is stored as BLOB. For showing logo
as picture format, the data of the logo decoded with given code below.

.. code-block:: python

    from base64 import b64encode

    logo = b64encode(temp_hotel.logo).decode("utf-8")

Update
______

Update hotel operation can be handled with given code below;

.. code-block:: python

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

As seen on code, there are two method for updating hotel table.

update_hotel method takes hotel_id and hotel class as parameter.
This method updates the hotel whose hotel_id is equal to taken hotel_id
with taken hotel class attributes but without logo attribute.

update_hotel_with_logo method takes hotel_id and hotel class as parameter.
This method updates the hotel whose hotel_id is equal to taken hotel_id
with taken hotel class attributes.

After update operations, hotel table will be updated.

Delete
______

Delete operation is handled with given code below;

.. code-block:: python


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

The deletion of hotel is handled with delete_hotel method. The selected hotel
will be deleted in hotels table by matching hotel_id taken as parameter.

The logo of hotel can be deleted without deleting the whole hotel information with
delete_hotel_logo method.
After delete_hotel_logo method, logo of the hotel will be NULL. The deletion of logo
is provided with matching hotel_id taken as parameter to this method.


Search
______

The search operation on hotel table is handled with given code below;

.. code-block:: python

    def search(self, text):
        hotels = []
        to_search = "%" + text + "%"
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM hotels JOIN city ON city.code = hotels.city WHERE (LOWER(name) like LOWER(%s)) or (LOWER(email) like LOWER(%s)) or (LOWER(description) like LOWER(%s)) or (LOWER(address) like LOWER(%s)) or (LOWER(website) like LOWER(%s)) or (LOWER(city_name) like LOWER(%s))    ;", (to_search, to_search, to_search, to_search, to_search, to_search))
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


The search method takes text as string. This string is searched in whole hotels table join with city table on city.
To search with case-insensitive string and whole data in hotels table
is used with LOWER function. This method returns array of tuple that has hotel_id and hotel
that has that string in anywhere on hotel information.

