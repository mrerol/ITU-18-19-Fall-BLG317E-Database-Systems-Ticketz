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
            cursor.execute("SELECT sale_price FROM sale where (current_date <= sale.sale_finish_at AND current_date >= sale.sale_start_at AND sale.firm_id = %s) AND sale.sale_id IN (SELECT sale_id FROM user_has_sale WHERE ( user_has_sale.sale_id = sale.sale_id AND user_has_sale.user_id = %s)) ", (firm_id,user_id,))
            sale_price = cursor.fetchone()
            cursor.close()
        return sale_price