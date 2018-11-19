import os
import sys

import psycopg2 as dbapi2

DATABASE_URL = 'postgres://kalcitdkfyeevw:39cdcacf84047dc48c74f58064a25a7406bd3645c95c712b9ba888f28cab791b@ec2-54-243-187-30.compute-1.amazonaws.com:5432/d96hqqveldfnft'

INIT_STATEMENTS = [
    """DROP TABLE IF EXISTS hotels""",
    """DROP TABLE IF EXISTS users""",
    """DROP TABLE IF EXISTS firms""",
    """DROP TABLE IF EXISTS drivers""",
    """DROP TABLE IF EXISTS vehicles""",

    """CREATE TABLE IF NOT EXISTS hotels 
    (
        hotel_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        email VARCHAR (50) NOT NULL,
        description VARCHAR (250) NOT NULL,
        city VARCHAR (20),
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        website VARCHAR (50)

    )""",

    """CREATE TABLE IF NOT EXISTS users 
    (
        user_id SERIAL NOT NULL PRIMARY KEY,
        email VARCHAR (50) NOT NULL,
        password VARCHAR (16) NOT NULL,
        name VARCHAR (50) NOT NULL,
        surname VARCHAR (50) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        gender VARCHAR (1) NOT NULL,
        address VARCHAR (250) NOT NULL,
        last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        register_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

    )""",

    """CREATE TABLE IF NOT EXISTS drivers 
    (
        driver_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        email VARCHAR (50) NOT NULL,
        gender VARCHAR (20) NOT NULL,
        city VARCHAR (20),
        vote VARCHAR (20),
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL

    )""",

    """CREATE TABLE IF NOT EXISTS firms 
    (
        firm_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        password VARCHAR (16) NOT NULL,
        email VARCHAR (50) NOT NULL,
        city VARCHAR (20),
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        website VARCHAR (50)

    )""",

    """CREATE TABLE IF NOT EXISTS vehicles 
    (
        vehicle_id SERIAL NOT NULL PRIMARY KEY,
        vehicle_type VARCHAR (20) NOT NULL,
        production_year VARCHAR (20) NOT NULL,
        recovery_year VARCHAR (20) NOT NULL,
        model VARCHAR (15) NOT NULL

    )""",

    """INSERT INTO hotels VALUES (
                        1,
                        'deneme',
                        'deneme@deneme.com',
                        'demo of description',
                        'istanbul',
                        'deneme sokak deneme cadde deneme',
                        '0321221222',
                        'dememe.com'

    )""",

    """INSERT INTO hotels VALUES (
                            2,
                            'deneme',
                            'deneme@deneme.com',
                            'demo of description',
                            'istanbul',
                            'deneme sokak deneme cadde deneme',
                            '0321221222',
                            'dememe.com'

        )""",

    """INSERT INTO hotels VALUES (
                            3,
                            'deneme',
                            'deneme@deneme.com',
                            'demo of description',
                            'istanbul',
                            'deneme sokak deneme cadde deneme',
                            '0321221222',
                            'dememe.com'

        )""",

    """INSERT INTO hotels VALUES (
                            4,
                            'deneme',
                            'deneme@deneme.com',
                            'demo of description',
                            'istanbul',
                            'deneme sokak deneme cadde deneme',
                            '0321221222',
                            'dememe.com'

        )""",

    """INSERT INTO hotels VALUES (
                            5,
                            'deneme',
                            'deneme@deneme.com',
                            'demo of description',
                            'istanbul',
                            'deneme sokak deneme cadde deneme',
                            '0321221222',
                            'dememe.com'

        )""",

    """INSERT INTO hotels VALUES (
                            6,
                            'deneme',
                            'deneme@deneme.com',
                            'demo of description',
                            'istanbul',
                            'deneme sokak deneme cadde deneme',
                            '0321221222',
                            'dememe.com'

        )"""

]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
