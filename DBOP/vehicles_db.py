from DBOP.tables.vehicles_table import Vehicle

import psycopg2 as dbapi2
import os

class vehicle_database:
    def __init__(self):
        self.vehicle = self.Vehicle()

    class Vehicle:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_vehicle(self, vehicle):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO vehicles ( name, category, model, capacity, production_year, production_place, description,firm_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (vehicle.name, vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.description, vehicle.firm_id))
                cursor.close()

        def add_vehicle_with_document(self, vehicle_with_doc):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO vehicles ( name, category, model, capacity, production_year, production_place, description,firm_id, document ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (vehicle_with_doc.name, vehicle_with_doc.category, vehicle_with_doc.model, vehicle_with_doc.capacity, vehicle_with_doc.production_year, vehicle_with_doc.production_place, vehicle_with_doc.description, vehicle_with_doc.firm_id, vehicle_with_doc.document))
                cursor.close()

        def get_vehicle_id(self, vehicle):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT vehicle_id FROM vehicles WHERE name = %s AND category = %s AND model = %s AND capacity = %s AND production_year = %s AND production_place = %s  AND description = %s ",
                    (vehicle.name, vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.description))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def get_firm_ids(self, vehicle_id):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM vehicles WHERE vehicle_id = %s ", (vehicle_id,))
                vehicles = cursor.fetchall()
                cursor.close()
                return vehicles

        def get_firm_id(self, vehicle_id):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM vehicles WHERE vehicle_id = %s ", (vehicle_id,))
                firm_id = cursor.fetchone()
                cursor.close()
                return firm_id

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
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8],vehicle[9])
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
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8],vehicle[9])
                    vehicles.append((vehicle[0], _vehicle))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return vehicles

        def get_vehicles_for_firms(self, firm_id):
            vehicles = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicles WHERE firm_id=%s;",(firm_id,))
                for vehicle in cursor:
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8],vehicle[9])
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
                cursor.execute("""UPDATE vehicles SET name = %s, category = %s, model = %s, capacity = %s, production_year = %s, production_place = %s, description = %s, firm_id = %s WHERE vehicle_id= %s """, (vehicle.name, vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place,vehicle.description, vehicle.firm_id, vehicle_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def update_vehicle_with_document(self, vehicle_id, vehicle):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE vehicles SET name = %s, category = %s, model = %s, capacity = %s, production_year = %s, production_place = %s, description = %s, firm_id = %s, document = %s WHERE vehicle_id = %s """, (vehicle.name, vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.description, vehicle.firm_id, vehicle.document, vehicle_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def delete_vehicle_document(self, vehicle_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("UPDATE vehicles SET document = NULL WHERE vehicle_id = %s", (vehicle_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()


        def search(self, text,firm_id):
            vehicles = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM vehicles  WHERE ((LOWER(name) like LOWER(%s)) or (LOWER(category) like LOWER(%s)) or (LOWER(model) like LOWER(%s)) or (LOWER(CAST(capacity AS VARCHAR )) like LOWER(%s)) or (LOWER(production_year) like LOWER(%s)) or (LOWER(production_place) like LOWER(%s)) or (LOWER(description) like LOWER(%s)) ) and firm_id = %s ;", (to_search, to_search, to_search, to_search, to_search, to_search,to_search,firm_id))
                for vehicle in cursor:
                    _vehicle = Vehicle(vehicle[1], vehicle[2], vehicle[3], vehicle[4], vehicle[5], vehicle[6], vehicle[7], vehicle[8],vehicle[9])
                    vehicles.append((vehicle[0], _vehicle))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return vehicles
