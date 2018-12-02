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
                    "INSERT INTO expeditions ( from_city, from_ter, to_city, to_ter, dep_time, arr_time, date, price, plane_id,total_cap, current_cap, driver_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.total_cap, expedition.current_cap, expedition.driver_id))
                cursor.close()

        def add_expedition_with_document(self, expedition):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO expeditions ( from_city, from_ter, to_city, to_ter, dep_time, arr_time, date, price, plane_id,total_cap, current_cap, driver_id, document) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (expedition.from_, expedition.from_ter, expedition.to, expedition.to_ter, expedition.dep_time, expedition.arr_time, expedition.date, expedition.price, expedition.selected_plane, expedition.total_cap, expedition.current_cap, expedition.driver_id, expedition.document ))
                cursor.close()
