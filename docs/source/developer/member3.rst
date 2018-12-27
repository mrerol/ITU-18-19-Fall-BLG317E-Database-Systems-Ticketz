Parts Implemented by Abdullah AKGÜL
===================================


deneme

Hotels Table
------------

deneme

Definition
^^^^^^^^^^

teble definition is given



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



Operations
^^^^^^^^^^

operations

Create
______

creation



.. code-block:: python

    def add_hotel(self, hotel):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO hotels ( name, email, description, city, address, phone, website) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website))
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


Expedition Table
-----------------

deneme

Definition
^^^^^^^^^^

teble definition is given



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



Operations
^^^^^^^^^^

operations

Create
______

creation



.. code-block:: python

    def add_hotel(self, hotel):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO hotels ( name, email, description, city, address, phone, website) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website))
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



Tickets Table
--------------

deneme

Definition
^^^^^^^^^^

teble definition is given



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



Operations
^^^^^^^^^^

operations

Create
______

creation



.. code-block:: python

    def add_hotel(self, hotel):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO hotels ( name, email, description, city, address, phone, website) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (hotel.name, hotel.email, hotel.description, hotel.city, hotel.address, hotel.phone, hotel.website))
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

