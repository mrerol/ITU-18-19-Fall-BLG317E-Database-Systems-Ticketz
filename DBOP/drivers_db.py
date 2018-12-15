from DBOP.tables.drivers_table import Driver

import psycopg2 as dbapi2
import os

class driver_database:
    def __init__(self):
        self.driver = self.Driver()

    class Driver:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_driver(self, driver):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO drivers ( name, email, gender, city, address, phone, firm_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone, driver.firm_id))
                cursor.close()


        def get_driver_id(self, driver):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT driver_id FROM drivers WHERE name = %s AND email = %s AND gender = %s AND city = %s AND address = %s AND phone= %s ",
                    (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def get_firm_ids(self, driver_id):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM drivers WHERE driver_id = %s ", (driver_id,))
                drivers = cursor.fetchall()
                cursor.close()
                return drivers


        def delete_driver(self, driver_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()


        def get_driver(self, driver_id):
            _driver = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
                driver = cursor.fetchone()
                if driver is not None:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _driver


        def get_drivers_for_firms(self, firm_id):
            drivers = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE (firm_id = %s)",(firm_id,))
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers

        def get_drivers(self):
            drivers = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers;")
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers

        def update_driver(self, driver_id, driver):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE drivers SET name = %s, email = %s, gender = %s, city = %s, address = %s, phone = %s, firm_id = %s WHERE driver_id= %s """, (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone, driver.firm_id, driver_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()


        def search(self, text):
            drivers = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE (name like %s)  or (email like %s) or (gender like %s) or (city like %s) or (address like %s)  or (phone like %s)  ;", (to_search, to_search, to_search, to_search, to_search, to_search))
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers
