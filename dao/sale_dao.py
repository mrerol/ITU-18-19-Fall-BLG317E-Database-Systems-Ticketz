import psycopg2 as dbapi2
import os
import sys
from .base_dao import BaseDao

class SaleDao(BaseDao):
    def __init__(self):
        super(SaleDao,self).__init__()

    def get_sale_price(self,firm_id,user_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT sale_price FROM sale where (current_date <= sale.sale_finish_at AND current_date >= sale.sale_start_at AND is_active = true AND sale.firm_id = %s) AND sale.sale_id IN (SELECT sale_id FROM user_has_sale WHERE ( user_has_sale.sale_id = sale.sale_id AND user_has_sale.user_id = %s)) ", (firm_id,user_id,))
            sale_price = cursor.fetchone()
            cursor.close()
        return sale_price

    def delete_sale(self, sale_id):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("DELETE FROM sale WHERE sale_id = %s", (sale_id,))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def edit_sale(self, sale_id,sale_code, sale_start_at, sale_finish_at, sale_description, is_active, firm_id, sale_price):
        try:
            connection = dbapi2.connect(self.url)
            cursor = connection.cursor()
            cursor.execute("""UPDATE sale SET sale_code = %s, sale_start_at = %s, sale_finish_at = %s, sale_description = %s, is_active = %s, firm_id = %s, sale_price = %s WHERE sale_id = %s """, (sale_code, sale_start_at, sale_finish_at, sale_description, is_active, firm_id, sale_price, sale_id,))
            connection.commit()
            cursor.close()
        except (Exception, dbapi2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def add_sale(self,sale_code, sale_start_at, sale_finish_at, sale_description, is_active, firm_id, sale_price):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO sale (sale_code, sale_start_at, sale_finish_at, sale_description, is_active, firm_id, sale_price) VALUES (%s, %s, %s, %s, %s, %s, %s) ", 
                (sale_code, sale_start_at, sale_finish_at, sale_description, is_active, firm_id, sale_price,))
            cursor.close()

    def get_all_sales(self):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT sale_id, sale_code,sale_start_at, sale_finish_at, sale_price, sale.firm_id,is_active FROM sale JOIN firms ON (sale.firm_id = firms.firm_id)")
            terminal = cursor.fetchall()
            cursor.close()
        return terminal

    def get_sale(self,sale_id):
        with dbapi2.connect(self.url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT sale_id, sale_code,sale_start_at, sale_finish_at, sale_price, sale.firm_id,is_active,sale_description FROM sale JOIN firms ON (sale.firm_id = firms.firm_id) WHERE sale.sale_id =%s",(sale_id,))
            terminal = cursor.fetchone()
            cursor.close()
        return terminal