import os
import sys

import psycopg2 as dbapi2

DATABASE_URL = 'postgres://kalcitdkfyeevw:39cdcacf84047dc48c74f58064a25a7406bd3645c95c712b9ba888f28cab791b@ec2-54-243-187-30.compute-1.amazonaws.com:5432/d96hqqveldfnft'

INIT_STATEMENTS = [
    #"""DROP TABLE IF EXISTS images""",
    #"""DROP TABLE IF EXISTS hotels""",
    """DROP TABLE IF EXISTS users""",
    """DROP TABLE IF EXISTS firms""",
    """DROP TABLE IF EXISTS drivers""",
    """DROP TABLE IF EXISTS vehicles""",
    """DROP TABLE IF EXISTS city""",

    """CREATE TABLE IF NOT EXISTS city 
    (
        code VARCHAR(2) UNIQUE NOT NULL PRIMARY KEY,
        city_name VARCHAR(25) UNIQUE NOT NULL        

    )""",

    """CREATE TABLE IF NOT EXISTS hotels 
    (
        hotel_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (25) NOT NULL,
        email VARCHAR (50) NOT NULL,
        description VARCHAR (250) NOT NULL,
        city VARCHAR(2),
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        website VARCHAR (50),
        logo BYTEA,
        FOREIGN KEY (city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS images(
        hotel_id INT NOT NULL,
        image_id SERIAL NOT NULL,
        file_data BYTEA,
        PRIMARY KEY (hotel_id, image_id),
        FOREIGN KEY (hotel_id) REFERENCES hotels (hotel_id) ON DELETE CASCADE ON UPDATE CASCADE ,
        UNIQUE (hotel_id, image_id)
    )
    """,

    """CREATE TABLE IF NOT EXISTS users 
    (
        user_id SERIAL NOT NULL PRIMARY KEY,
        user_name VARCHAR(15) UNIQUE NOT NULL,
        email VARCHAR (50) NOT NULL,
        password VARCHAR (16) NOT NULL,
        name VARCHAR (50) NOT NULL,
        surname VARCHAR (50) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        gender VARCHAR (1) NOT NULL,
        address VARCHAR (250) NOT NULL,
        last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        register_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE

    )""",


    """CREATE TABLE IF NOT EXISTS terminal 
    (
        terminal_id SERIAL NOT NULL PRIMARY KEY,
        terminal_name VARCHAR(50) UNIQUE NOT NULL,
        terminal_code VARCHAR(6) UNIQUE NOT NULL,
        email VARCHAR (50) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        address VARCHAR (250) NOT NULL,
        description VARCHAR (60) NOT NULL,
        city_id VARCHAR (2)
        FOREIGN KEY (city_id) REFERENCES city (code) ON DELETE CASCADE ON UPDATE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS drivers 
    (
        driver_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        email VARCHAR (50) NOT NULL,
        gender VARCHAR (20) NOT NULL,
        city VARCHAR (20) NOT NULL,
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        vote_number VARCHAR (20),
        score VARCHAR (20)

    )""",

    """CREATE TABLE IF NOT EXISTS firms 
    (
        firm_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        password VARCHAR (16) NOT NULL,
        email VARCHAR (50) NOT NULL,
        city VARCHAR (20) NOT NULL,
        address VARCHAR (250) NOT NULL,
        phone VARCHAR (15) NOT NULL,
        website VARCHAR (50) NOT NULL,
        description VARCHAR (250),
        logo VARCHAR (50) 

    )""",

    """CREATE TABLE IF NOT EXISTS vehicles 
    (
        vehicle_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (50) NOT NULL,
        category VARCHAR (50) NOT NULL,
        model VARCHAR (15) NOT NULL,
        capacity VARCHAR (50) NOT NULL,
        production_year VARCHAR (20) NOT NULL,
        production_place VARCHAR (20) NOT NULL,
        recovery_time VARCHAR (20) NOT NULL,
        description VARCHAR (250),
        image VARCHAR (50)

    )""",

    """INSERT INTO drivers VALUES (
                        1,
                        'rasit',
                        'rasit@rasit.com',
                        'true',
                        'istanbul',
                        'deneme sokak deneme cadde deneme',
                        '0321221222',
                        '100',
                        '6'

    )""",

    """INSERT INTO vehicles VALUES (
                        1,
                        'Safiye Soyman',
                        'yuruyen ucak',
                        'X2342SD',
                        '500',
                        '1920',
                        'istabul',
                        '2020',
                        'guzel',
                        'image'

    )""",

    """INSERT INTO firms VALUES (
                        1,
                        'itu',
                        'parola',
                        'deneme@deneme.com',
                        'istanbul',
                        'deneme sokak deneme cadde deneme',
                        '0321221222',
                        'dememe.com',
                        'aciklama'

    )""",

    """INSERT INTO city VALUES 
                            ('01', 'Adana'),
                            ('02', 'Adıyaman'),
                            ('03', 'Afyon'),
                            ('04', 'Ağrı'),
                            ('05', 'Amasya'),
                            ('06', 'Ankara'),
                            ('07', 'Antalya'),
                            ('08', 'Artvin'),
                            ('09', 'Aydın'),
                            ('10', 'Balıkesir'),
                            ('11', 'Bilecik'),
                            ('12', 'Bingöl'),
                            ('13', 'Bitlis'),
                            ('14', 'Bolu'),
                            ('15', 'Burdur'),
                            ('16', 'Bursa'),
                            ('17', 'Çanakkale'),
                            ('18', 'Çankırı'),
                            ('19', 'Çorum'),
                            ('20', 'Denizli'),
                            ('21', 'Diyarbakır'),
                            ('22', 'Edirne'),
                            ('23', 'Elazığ'),
                            ('24', 'Erzincan'),
                            ('25', 'Erzurum'),
                            ('26', 'Eskişehir'),
                            ('27', 'Gaziantep'),
                            ('28', 'Giresun'),
                            ('29', 'Gümüşhane'),
                            ('30', 'Hakkari'),
                            ('31', 'Hatay'),
                            ('32', 'Isparta'),
                            ('33', 'Mersin'),
                            ('34', 'İstanbul'),
                            ('35', 'İzmir'),
                            ('36', 'Kars'),
                            ('37', 'Kastamonu'),
                            ('38', 'Kayseri'),
                            ('39', 'Kırklareli'),
                            ('40', 'Kırşehir'),
                            ('41', 'Kocaeli'),
                            ('42', 'Konya'),
                            ('43', 'Kütahya'),
                            ('44', 'Malatya'),
                            ('45', 'Manisa'),
                            ('46', 'K.Maraş'),
                            ('47', 'Mardin'),
                            ('48', 'Muğla'),
                            ('49', 'Muş'),
                            ('50', 'Nevşehir'),
                            ('51', 'Niğde'),
                            ('52', 'Ordu'),
                            ('53', 'Rize'),
                            ('54', 'Sakarya'),
                            ('55', 'Samsun'),
                            ('56', 'Siirt'),
                            ('57', 'Sinop'),
                            ('58', 'Sivas'),
                            ('59', 'Tekirdağ'),
                            ('60', 'Tokat'),
                            ('61', 'Trabzon'),
                            ('62', 'Tunceli'),
                            ('63', 'Şanlıurfa'),
                            ('64', 'Uşak'),
                            ('65', 'Van'),
                            ('66', 'Yozgat'),
                            ('67', 'Zonguldak'),
                            ('68', 'Aksaray'),
                            ('69', 'Bayburt'),
                            ('70', 'Karaman'),
                            ('71', 'Kırıkkale'),
                            ('72', 'Batman'),
                            ('73', 'Şırnak'),
                            ('74', 'Bartın'),
                            ('75', 'Ardahan'),
                            ('76', 'Iğdır'),
                            ('77', 'Yalova'),
                            ('78', 'Karabük'),
                            ('79', 'Kilis'),
                            ('80', 'Osmaniye'),
                            ('81', 'Düzce')

        """

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
