from DBOP.tables.vehicles_table import Vehicle

import psycopg2 as dbapi2
import os

class vehicle_database:
    def __init__(self):
        self.vehicle = self.Vehicle()

    class Vehicle:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32770/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_vehicle(self, vehicle):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO vehicles ( category, model, capacity, production_year, production_place, recovery_time, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.recovery_time, vehicle.description, vehicle.image))
                cursor.close()

        def add_vehicle_with_image(self, vehicle_with_logo):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO vehicles ( category, model, capacity, production_year, production_place, recovery_time, description, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (vehicle_with_logo.category, vehicle_with_logo.model, vehicle_with_logo.capacity, vehicle_with_logo.production_year, vehicle_with_logo.production_place, vehicle_with_logo.recovery_time, vehicle_with_logo.description, vehicle_with_logo.image))
                cursor.close()

        def get_vehicle_id(self, vehicle):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT vehicle_id FROM vehicles WHERE category = %s AND model = %s AND capacity = %s AND production_year = %s AND production_place = %s AND recovery_time= %s AND description = %s ",
                    (vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.recovery_time, vehicle.description))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def delete_vehicle(self, vehicle_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM vehicles WHERE vehicle_id = %s", (vehicle_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def delete_vehicle_image(self, vehicle_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("UPDATE vehicles SET image = NULL WHERE vehicle_id = %s", (vehicle_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_vehicle(self, vehicle_id):
            _vehicle = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicles WHERE vehicle_id = %s", (vehicle_id,))
                vehicle = cursor.fetchone()
                if vehicle is not None:
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _vehicle

        def get_vehicles(self):
            vehicles = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicles;")
                for vehicle in cursor:
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8])
                    vehicles.append((vehicle[0], _vehicle))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return vehicles

        def update_vehicle(self, vehicle_id, vehicle):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                statement = """UPDATE vehicles SET category = '""" + vehicle.category + """' , model = '""" + vehicle.model +"""' , capacity = '""" + vehicle.capacity + """', production_year = ' """ + vehicle.production_year +"""' ,  production_place = '""" + vehicle.production_place + """', recovery_time = '""" + vehicle.recovery_time +"""', description = '""" + vehicle.description + """'  WHERE vehicle_id = """ + str(vehicle_id)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def update_vehicle_with_image(self, vehicle_id, vehicle):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE vehciles SET category = %s, model = %s, capacity = %s, production_year = %s, production_place = %s, recovery_time = %s, description = %s, image = %s WHERE vehicle_id = %s """, (vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.recovery_time, vehicle.description, vehicle.image, vehicle_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def search(self, text):
            vehicles = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicles WHERE (category like %s)  or (model like %s) or (capacity like %s) or (production_year like %s) or (production_place like %s)  or (recovery_time like %s) or (description like %s) ;", (to_search, to_search, to_search, to_search, to_search, to_search,to_search))
                for vehicle in cursor:
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7])
                    vehicles.append((vehicle[0], _vehicle))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return vehicles
