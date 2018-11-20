import psycopg2 as dbapi2
import os
import sys

class BaseDao(object):
    def __init__(self):
        self.url = os.getenv("DATABASE_URL")
        #self.url = "user=postgres password=1234 host=localhost port=5432 dbname=ticketzdb"