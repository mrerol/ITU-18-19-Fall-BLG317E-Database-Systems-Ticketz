from DBOP.tables.seat_table import Seat
import psycopg2 as dbapi2
import os


class seat_database:
    def __init__(self):
        self.seat = self.Seat()

    class Seat:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_seat(self, seat):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO seats ( expedition_id, user_id, seat_number) VALUES (%s, %s, %s)",
                    (seat.expedition_id, seat.user_id, seat.seat_number))
                cursor.close()

        def delete_seat(self, seat):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM seats WHERE expedition_id = %s AND user_id = %s AND seat_number = %s", (seat.expedition_id, seat.user_id, seat.seat_number))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_seats_of_expedition(self, expedition_id):
            seats = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM seats WHERE expedition_id = %s;", (expedition_id, ) )
                for seat in cursor:
                    _seat = Seat(seat[0], seat[1], seat[2])
                    seats.append(_seat)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return seats

        def get_seat_of_user(self, expedition_id, user_id):
            seats = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM seats WHERE expedition_id = %s AND user_id = %s;", (expedition_id, user_id ) )
                for seat in cursor:
                    _seat = Seat(seat[0], seat[1], seat[2])
                    seats.append(_seat)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return seats

        def update_seat_number(self, seat, new_seat_number):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE seats SET seat_number = %s WHERE expedition_id = %s AND user_id = %s AND seat_number = %s """, ( new_seat_number, seat.expedition_id, seat.user_id, seat.seat_number))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
