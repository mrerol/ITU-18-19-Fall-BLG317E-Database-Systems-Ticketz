from DBOP.tables.ticket_table import Ticket
import psycopg2 as dbapi2
import os

def isInt(value):
  try:
    int(value)
    return True
  except ValueError:
    return False


class ticket_database:
    def __init__(self):
        self.ticket = self.Ticket()

    class Ticket:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_ticket(self, ticket):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO tickets ( expedition_id, user_id, seat_number, is_cancelable, extra_baggage, firm_id, price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (ticket.expedition_id, ticket.user_id, ticket.seat_number, ticket.is_cancelable, ticket.extra_baggage, ticket.firm_id, ticket.price))
                cursor.close()

        def delete_ticket(self, ticket_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM tickets WHERE ticket_id = %s", (ticket_id, ))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_tickets_of_users(self, user_id):
            tickets = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM tickets WHERE user_id = %s;", (user_id, ) )
                for ticket in cursor:
                    _ticket = Ticket(ticket[0], ticket[1], ticket[2], ticket[9], ticket[8], ticket[7], ticket[6], ticket[4], ticket[5])
                    tickets.append((ticket[3], _ticket))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return tickets

        def get_ticket(self, ticket_id):
            tickets = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM tickets WHERE ticket_id = %s;", (ticket_id, ) )
                for ticket in cursor:
                    _ticket = Ticket(ticket[0], ticket[1], ticket[2], ticket[9], ticket[8], ticket[7], ticket[6], ticket[4], ticket[5])
                    tickets.append(_ticket)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return tickets

        def update_ticket(self, ticket,new_seat_number, new_cancel, new_baggage):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE tickets SET seat_number = %s, is_cancelable = %s, extra_baggage = %s, edited_at = CURRENT_TIMESTAMP WHERE expedition_id = %s AND user_id = %s AND seat_number = %s """, ( new_seat_number, new_cancel, new_baggage ,ticket.expedition_id, ticket.user_id, new_seat_number))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def search(self, text):
            tickets = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                if isInt(text):

                    cursor.execute("""select * from tickets where ticket_id in (
                                    select ticket_id
                                    from tickets, expeditions, city as to_city, firms, city as from_city, terminal as to_ter, terminal as from_ter 
                                    where (firms.firm_id = tickets.firm_id and expeditions.to_city = to_city.code and expeditions.from_city = from_city.code and expeditions.to_ter = to_ter.terminal_id and expeditions.from_ter = from_ter.terminal_id ) 
                                    and 
                                    ( (tickets.price = %s) or (LOWER(to_city.city_name) like LOWER(%s)) or ( LOWER(firms.name) like LOWER(%s) ) or ( LOWER(from_city.city_name) like LOWER(%s) ) or (LOWER(date) like LOWER(%s)) or (LOWER(dep_time) like LOWER(%s)) or (LOWER(arr_time) like LOWER(%s)) or (LOWER(from_ter.terminal_name) like LOWER(%s)) or (LOWER(to_ter.terminal_name) like LOWER(%s))))""", (int(text) ,to_search, to_search, to_search, to_search, to_search, to_search,to_search,to_search, ))
                else:
                    cursor.execute("""select * from tickets where ticket_id in (
                                    select ticket_id
                                    from tickets, city as to_city, firms, city as from_city, terminal as to_ter, terminal as from_ter 
                                    where (firms.firm_id = tickets.firm_id and expeditions.to_city = to_city.code and expeditions.from_city = from_city.code and expeditions.to_ter = to_ter.terminal_id and expeditions.from_ter = from_ter.terminal_id ) 
                                    and 
                                    (  (LOWER(to_city.city_name) like LOWER(%s)) or ( LOWER(firms.name) like LOWER(%s) ) or ( LOWER(from_city.city_name) like LOWER(%s) ) or (LOWER(date) like LOWER(%s)) or (LOWER(dep_time) like LOWER(%s)) or (LOWER(arr_time) like LOWER(%s)) or (LOWER(from_ter.terminal_name) like LOWER(%s)) or (LOWER(to_ter.terminal_name) like LOWER(%s))))""",
                                   ( to_search, to_search, to_search, to_search, to_search, to_search, to_search,
                                    to_search,))

                for ticket in cursor:
                    _ticket = Ticket(ticket[0], ticket[1], ticket[2], ticket[9], ticket[8], ticket[7], ticket[6], ticket[4], ticket[5])
                    tickets.append((ticket[3], _ticket))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return tickets