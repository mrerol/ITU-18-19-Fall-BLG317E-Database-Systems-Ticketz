import os
import sys

import psycopg2 as dbapi2

DATABASE_URL = 'postgres://kalcitdkfyeevw:39cdcacf84047dc48c74f58064a25a7406bd3645c95c712b9ba888f28cab791b@ec2-54-243-187-30.compute-1.amazonaws.com:5432/d96hqqveldfnft'

INIT_STATEMENTS = [
    #"""DROP TABLE IF EXISTS images""",
    #"""DROP TABLE IF EXISTS hotels""",
    """DROP TABLE IF EXISTS users cascade """,
    """DROP TABLE IF EXISTS firms cascade""",
    """DROP TABLE IF EXISTS drivers cascade""",
    """DROP TABLE IF EXISTS vehicles cascade""",
    """DROP TABLE IF EXISTS city cascade""",
    """DROP TABLE IF EXISTS sale cascade""",
    """DROP TABLE IF EXISTS terminal cascade""",
    """DROP TABLE IF EXISTS user_has_sale cascade""",

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
        city_id VARCHAR (2),
        FOREIGN KEY (city_id) REFERENCES city (code) ON DELETE CASCADE ON UPDATE CASCADE

    )""",

    """CREATE TABLE IF NOT EXISTS firms 
    (
        firm_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (20) NOT NULL,
        password VARCHAR (20) NOT NULL,
        email VARCHAR (20) NOT NULL,
        phone VARCHAR (20) NOT NULL,
        city VARCHAR (2),
        address VARCHAR (100),
        website VARCHAR (20),
        description VARCHAR (200),
        logo BYTEA,
        FOREIGN KEY (city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE
    
    )""",

    """CREATE TABLE IF NOT EXISTS drivers 
    (
        driver_id SERIAL NOT NULL PRIMARY KEY,
        name VARCHAR (20) NOT NULL,
        email VARCHAR (20) NOT NULL,
        gender VARCHAR (20),
        city VARCHAR (2),
        address VARCHAR (200),
        phone VARCHAR (20) NOT NULL,
        vote_number VARCHAR (20),
        score VARCHAR (20),
        logo BYTEA,
        firm_id INT,
        FOREIGN KEY (city) REFERENCES city (code) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (firm_id) REFERENCES firms (firm_id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",

    """CREATE TABLE IF NOT EXISTS vehicles 
      (
          vehicle_id SERIAL NOT NULL PRIMARY KEY,
          name VARCHAR (20) NOT NULL,
          category VARCHAR (20) NOT NULL,
          model VARCHAR (20) NOT NULL,
          capacity INT NOT NULL,
          production_year VARCHAR (20) NOT NULL,
          production_place VARCHAR (20) NOT NULL,
          recovery_time VARCHAR (20) NOT NULL,
          description VARCHAR (200),
          image VARCHAR (50),
          driver_id INT,
          firm_id INT,
          FOREIGN KEY (driver_id) REFERENCES drivers (driver_id),
          FOREIGN KEY (firm_id) REFERENCES firms (firm_id)
    
      )""",

    """CREATE TABLE IF NOT EXISTS expeditions 
    (
        expedition_id SERIAL NOT NULL PRIMARY KEY,
        from_city VARCHAR (02) NOT NULL,
        from_ter INT NOT NULL,
        to_city VARCHAR (02) NOT NULL,
        to_ter INT NOT NULL,
        dep_time VARCHAR (5) NOT NULL ,
        arr_time VARCHAR (5) NOT NULL ,
        date VARCHAR (10) NOT NULL ,
        price INT NOT NULL CHECK (price >= 10),
        plane_id INT NOT NULL ,
        current_cap INT NOT NULL DEFAULT 0,
        total_cap INT NOT NULL,
        driver_id INT NOT NULL,
        firm_id INT NOT NULL,
        document BYTEA,
        FOREIGN KEY (from_city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (to_city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (from_ter) REFERENCES terminal (terminal_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (to_ter) REFERENCES terminal (terminal_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (plane_id) REFERENCES vehicles (vehicle_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (driver_id) REFERENCES drivers (driver_id) ON DELETE RESTRICT ON UPDATE CASCADE,
        FOREIGN KEY (firm_id) REFERENCES firms (firm_id) ON DELETE RESTRICT ON UPDATE CASCADE
        

    )""",

    """CREATE TABLE IF NOT EXISTS seats(
        expedition_id INT NOT NULL,
        user_id INT NOT NULL,
        seat_number INT NOT NULL,
        PRIMARY KEY (expedition_id, user_id, seat_number),
        FOREIGN KEY (expedition_id) REFERENCES expeditions (expedition_id) ON DELETE RESTRICT ON UPDATE CASCADE ,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE ,
        UNIQUE (expedition_id, user_id, seat_number)
    )
    """,

    """CREATE TABLE IF NOT EXISTS tickets(
        expedition_id INT NOT NULL,
        user_id INT NOT NULL,
        seat_number INT NOT NULL,
        ticket_id SERIAL NOT NULL,
        bought_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_cancelable BOOLEAN DEFAULT FALSE,
        extra_baggage BOOLEAN DEFAULT FALSE,
        UNIQUE (expedition_id, user_id, seat_number),
        PRIMARY KEY (ticket_id),
        FOREIGN KEY (expedition_id, user_id, seat_number) REFERENCES seats (expedition_id, user_id, seat_number) ON DELETE RESTRICT ON UPDATE CASCADE     
    )
    """,

    """CREATE TABLE IF NOT EXISTS sale(
        sale_id SERIAL NOT NULL PRIMARY KEY,
        sale_code VARCHAR(6) UNIQUE NOT NULL,
        sale_start_at DATE NOT NULL,
        sale_finish_at DATE NOT NULL,
        sale_description VARCHAR (60) NOT NULL,
        is_active BOOLEAN NOT NULL,
        firm_id INT NOT NULL,
        FOREIGN KEY (firm_id) REFERENCES firms (firm_id) ON DELETE CASCADE ON UPDATE CASCADE
    )""",

    """CREATE TABLE IF NOT EXISTS user_has_sale(
        sale_id INT NOT NULL,
        user_id INT NOT NULL,
        is_used BOOLEAN NOT NULL,
        PRIMARY KEY (sale_id, user_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (sale_id) REFERENCES sale (sale_id) ON DELETE CASCADE ON UPDATE CASCADE
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
    
        """,

    """INSERT INTO terminal VALUES(5,'3de3m2','3d112','3email','3phone2','addres2s','descrip2tion','01')""",

    """INSERT INTO terminal VALUES(6,'3devm2','3d1n12', '3emadil', '3phodne2','addres2s','descrip2tion', '01')""",

    """ INSERT INTO firms
        (firm_id, name, "password", email, phone, city, address, website, description, logo)
        VALUES(100, 'deneme', 'deneme', 'deneme', '23452345', '10', NULL, NULL, NULL, NULL);
    """,

    """ INSERT INTO firms
        (firm_id, name, "password", email, phone, city, address, website, description, logo)
        VALUES(101, 'deneme1', 'deneme1', 'deneme1', '234523245', '10', NULL, NULL, NULL, NULL);
    """,

    """ INSERT INTO firms
        (firm_id, name, "password", email, phone, city, address, website, description, logo)
        VALUES(102, 'deneme2', 'deneme2', 'deneme1', '234523245', '10', NULL, NULL, NULL, NULL);
    """,

    """ INSERT INTO drivers 
        (driver_id, name, email, gender, city, address, phone, vote_number, score, logo, firm_id)
        VALUES(100, 'driver', 'driver', 'kadin','10', 'address', '123123', NULL, NULL, NULL,100);
    """,

    """ INSERT INTO drivers 
        (driver_id, name, email, gender, city, address, phone, vote_number, score, logo, firm_id)
        VALUES(101, 'driver', 'driver', 'kadin','10', 'address', '123123', NULL, NULL, NULL,100);
    """,

    """ INSERT INTO drivers 
        (driver_id, name, email, gender, city, address, phone, vote_number, score, logo, firm_id)
        VALUES(102, 'driver', 'driver', 'kadin','10', 'address', '123123', NULL, NULL, NULL,101);
    """,

    """INSERT INTO vehicles
        (vehicle_id, name, category, model, capacity, production_year, production_place, recovery_time, description, image, driver_id, firm_id)
        VALUES(100, 'Safiye Soyman', 'yuruyen ucak', 'X2342SD', 500, '1920', 'istabul', '2020', 'guzel', 'image', 100, 100);
""",

    """INSERT INTO vehicles
        (vehicle_id, name, category, model, capacity, production_year, production_place, recovery_time, description, image, driver_id, firm_id)
        VALUES(101, 'Safiye Soyman', 'yuruyen ucak', 'X2342SD', 500, '1920', 'istabul', '2020', 'guzel', 'image', 102, 101);
""",

    """INSERT INTO users VALUES (
                        1,
                        'admin',
                        'admin@admin.com',
                        'admin',
                        'admin',
                        'admin',
                        '0321221222',
                        '1',
                        'deneme sokak deneme cadde deneme',
                        '2017-08-02 12:10:11.123456',
                        '2017-08-02 12:10:11.123456',
                        'true'
    
    )""",

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
