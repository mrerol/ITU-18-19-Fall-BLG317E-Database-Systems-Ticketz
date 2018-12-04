from DBOP.tables.expedition_table import Expedition

import psycopg2 as dbapi2
import os


class expedition_database:
    def __init__(self):
        self.expedition = self.Expedition()

    class Expedition:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_expedition(self, expedition):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO expeditions ( from_city, from_ter, to_city, to_ter, dep_time, arr_time, date, price, plane_id, firm_id, total_cap, current_cap, driver_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.firm_id,expedition.total_cap, expedition.current_cap, expedition.driver_id))
                cursor.close()

        def add_expedition_with_document(self, expedition):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO expeditions ( from_city, from_ter, to_city, to_ter, dep_time, arr_time, date, price, plane_id, firm_id, total_cap, current_cap, driver_id, document) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.firm_id, expedition.total_cap, expedition.current_cap, expedition.driver_id, expedition.document ))
                cursor.close()

        def update_expedition(self, expedition_id, expedition):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE expeditions SET from_city = %s, from_ter = %s, to_city = %s, to_ter = %s, dep_time = %s, arr_time = %s, date = %s, price = %s, plane_id = %s, firm_id = %s, total_cap = %s, current_cap = %s, driver_id = %s WHERE expedition_id = %s",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.firm_id,expedition.total_cap, expedition.current_cap, expedition.driver_id, expedition_id))
                cursor.close()

        def update_expedition_with_document(self, expedition_id, expedition):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE expeditions SET from_city = %s, from_ter = %s, to_city = %s, to_ter = %s, dep_time = %s, arr_time = %s, date = %s, price = %s, plane_id = %s, firm_id = %s, total_cap = %s, current_cap = %s, driver_id = %s, document = %s WHERE expedition_id = %s",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.firm_id, expedition.total_cap, expedition.current_cap, expedition.driver_id, expedition.document, expedition_id))
                cursor.close()


        def get_all_expeditions(self):
            expeditions = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM expeditions;")
                for expedition in cursor:
                    _expedition = Expedition(expedition[1], expedition[2], expedition[3], expedition[4], expedition[5],
                                             expedition[6], expedition[7], expedition[8], expedition[9], expedition[12],
                                             expedition[13], expedition[11], expedition[10], expedition[14])
                    expeditions.append((expedition[0], _expedition))
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return expeditions

        def get_firms_expedition(self, firm_id):
            expeditions = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM expeditions WHERE firm_id = %s;", (firm_id,))
                for expedition in cursor:
                    _expedition = Expedition(expedition[1], expedition[2], expedition[3], expedition[4], expedition[5],
                                             expedition[6], expedition[7], expedition[8], expedition[9], expedition[12],
                                             expedition[13], expedition[11], expedition[10], expedition[14])
                    expeditions.append((expedition[0], _expedition))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print("hata")
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return expeditions


        def get_expedition(self, expedition_id):
            _expedition = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM expeditions WHERE expedition_id = %s", (expedition_id,))
                expedition = cursor.fetchone()
                if expedition is not None:
                    _expedition = Expedition(expedition[1], expedition[2], expedition[3], expedition[4], expedition[5],
                                             expedition[6], expedition[7], expedition[8], expedition[9], expedition[12],
                                             expedition[13], expedition[11], expedition[10], expedition[14])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _expedition

        def delete_expedition_document(self, expedition_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("UPDATE expeditions SET document = NULL WHERE expedition_id = %s", (expedition_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def delete_expedition(self, expedition_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM expeditions WHERE expedition_id = %s", (expedition_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()