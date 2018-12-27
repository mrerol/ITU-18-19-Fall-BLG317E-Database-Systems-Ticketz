Parts Implemented by Muhammed Raşit EROL
========================================

In this section, there are three main tables which are firms, drivers and vehicles; moreover,
images_for_firms table is extra table.
The responsibility of these tables belongs to Muhammed Raşit EROL.
Attributes of tables which are mentioned above can be seen in Figure 1.

Furthermore, ER diagrams of all tables can be seen in
Figure 2, Figure 2, Figure 3, Figure 4 and Figure 5.

firms Table
------------

firms table is created for adding and editing expeditions.
Hence, a user is able to see expeditions which are created by firms.
In order organize that operations, firms table is developed as another users table.
However, instead of storing detailed user information, firms table stores information
which are useful for viewing expeditions. Thus, a user can visit firm page which is appeared
in the expedition card. However, main duty of the firms is creating and editing expeditions
which are appears in the user main page. In order the perform that,
email and password attributes are used in the firms table. Other attributes
which are name, phone, city, address, website, description and logo, are used for
getting detailed information when visiting the firm page. The attribute city is used as
foreign key. Also, logo is stored as BLOB type in the database. Moreover,
email and password cannot be NULL because a firm must have these attributes
due to the proper login; furthermore, name and phone cannot be NULL
due to need of at least one contact information and reason for
illogical situation if there is no name for a firm. Also, firm_id is primary key
for firms table and its serially increased by the system. The creation code of
the firms table can be seen below.



.. code-block:: sql

CREATE TABLE IF NOT EXISTS firms
    (
        firm_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (20) NOT NULL,
        password VARCHAR (50) NOT NULL,
        email VARCHAR (20) NOT NULL,
        phone VARCHAR (20) NOT NULL,
        city VARCHAR (2),
        address VARCHAR (100),
        website VARCHAR (20),
        description VARCHAR (200),
        logo BYTEA,
        FOREIGN KEY (city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE

    )

All operations of the firms table can be seen below:

Operations
^^^^^^^^^^

Creating, reading, updating and deleting operations can be performed on the firms table.

The attributes of the firms table correspond the parameters on the Firm class.
Hence, with this approach, it is easy to manage the data which stands for attributes of the firms table.
The Firm class can be seen below:

.. code-block:: python

    class Firm:
        def __init__(self, name, password, email, phone, city, address, website, description, logo=None):
            self.name = name
            self.password = password
            self.email = email
            self.phone = phone
            self.city = city
            self.address = address
            self.website = website
            self.description = description
            self.logo = logo


The attributes of the firms table correspond the parameters on the Firm class.
Hence, with this approach, it is easy to manage the data which stands for attributes of the firms table.
Also, firm_database class is another class which is used for performing table operations with the methods of the Firm class.
The example add_firm method of Firm class can be seen in the below code. Furthermore, database connection is handled with that class.
Hence, in the firm_database class, all data and methods can be used with the Firm class. Thus, all database operations
are handled with the object oriented approach. The code of firm_database and Firm class can be seen below.

.. code-block:: python

    class firm_database:
        def __init__(self):
            self.firm = self.Firm()

        class Firm:
            def __init__(self):
                if os.getenv("DATABASE_URL") is None:
                    self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
                else:
                    self.url = os.getenv("DATABASE_URL")

            def add_firm(self, firm):
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO firms ( name, password, email, phone, city, address, website, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (firm.name, firm.password, firm.email, firm.phone, firm.city, firm.address, firm.website, firm.description))
                    cursor.close()

Insert
______



.. code-block:: python

        def add_firm(self, firm):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, phone, city, address, website, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (firm.name, firm.password, firm.email, firm.phone, firm.city, firm.address, firm.website, firm.description))
                cursor.close()

        def add_firm_with_logo(self, firm_with_logo):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, phone, city, address, website, description, logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (firm_with_logo.name, firm_with_logo.password, firm_with_logo.email, firm_with_logo.phone, firm_with_logo.city, firm_with_logo.address, firm_with_logo.website,firm_with_logo.description, firm_with_logo.logo))
                cursor.close()


Read
____

read



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

Update
______

update

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


Delete
______

delete

.. code-block:: python

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

Related Systems
^^^^^^^^^^^^^^^

Search
______

search

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

