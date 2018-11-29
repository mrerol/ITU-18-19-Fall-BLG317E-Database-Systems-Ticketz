from DBOP.tables.firms_table import Firm

import psycopg2 as dbapi2
import os

class firm_database:
    def __init__(self):
        self.firm = self.Firm()

    class Firm:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32770/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_firm(self, firm):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, city, address, phone, website, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (firm.name, firm.password, firm.email, firm.city, firm.address, firm.phone, firm.website, firm.description))
                cursor.close()

        def add_firm_with_logo(self, firm_with_logo):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, city, address, phone, website, description, logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s))",
                    (firm_with_logo.name, firm_with_logo.password, firm_with_logo.email, firm_with_logo.city, firm_with_logo.address, firm_with_logo.phone, firm_with_logo.website,
                     firm_with_logo.description, firm_with_logo.logo))
                cursor.close()


        def get_firm_id(self,firm):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM firms WHERE name = %s AND password = %s AND email = %s AND city = %s AND address = %s AND phone= %s AND website = %s AND description = %s",
                    (firm.name, firm.password, firm.email, firm.city, firm.address, firm.phone, firm.website,
                     firm.description))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def delete_firm(self, firm_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM firms WHERE firm_id = %s", (firm_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def delete_firm_logo(self, firm_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("UPDATE firms SET logo = NULL WHERE firm_id = %s", (firm_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_firm(self, firm_id):
            _firm = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM firms WHERE firm_id = %s", (firm_id,))
                firm = cursor.fetchone()
                if firm is not None:
                    _firm = Firm(firm[1], firm[2], firm[3], firm[4], firm[5], firm[6], firm[7], firm[8], firm[9])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _firm

        def get_firms(self):
            firms = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM firms;")
                for firm in cursor:
                    _firm = Firm(firm[1], firm[2], firm[3], firm[4], firm[5], firm[6], firm[7], firm[8], firm[9])
                    firms.append((firm[0], _firm))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return firms

        def update_firm(self, firm_id, firm):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                statement = """UPDATE firms SET name = '""" + firm.name + """' , password = '""" + firm.password +"""' , email = '""" + firm.email + """', city = ' """ + firm.city +"""' ,  address = '""" + firm.address + """', phone = '""" + firm.phone +"""', website = '""" + firm.website + """', description = '""" + firm.description + """', logo = '""" + firm.logo + """'     WHERE firm_id = """ + str(firm_id)
                cursor.execute(statement)
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def update_firm_with_logo(self, firm_id, firm):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE firms SET name = %s, password = %s, email = %s, city = %s, address = %s, phone = %s, website = %s, description = %s, logo = %s WHERE firm_id = %s """, (firm.name, firm.password, firm.email, firm.city, firm.address, firm.phone, firm.website, firm.descrpition, firm.logo, firm_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def search(self, text):
            firms = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM firms WHERE (name like %s)  or (email like %s) or (city like %s) or (address like %s)  or (phone like %s) or (website like %s) or (description like %s) or (logo like %s)      ;", (to_search, to_search, to_search, to_search, to_search, to_search,to_search,to_search))
                for firm in cursor:
                    _firm = Firm(firm[1], firm[3], firm[4], firm[5], firm[6], firm[7], firm[8], firm[9])
                    firms.append((firm[0], _firm))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return firms
