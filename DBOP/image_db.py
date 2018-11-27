from DBOP.tables.image_table import Image
import psycopg2 as dbapi2
import os


class image_database:
    def __init__(self):
        self.image = self.Image()

    class Image:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_image(self, image):
            print("database")
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO images ( hotel_id, file_data) VALUES (%s, %s)",
                    (image.hotel_id, image.file_data))
                cursor.close()

        def delete_image(self, hotel_id, image_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM images WHERE hotel_id = %s AND image_id = %s", (hotel_id, image_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_image(self, hotel_id, image_id):
            _image = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM images WHERE hotel_id = %s AND image_id = %s", (hotel_id, image_id,))
                image = cursor.fetchone()
                if image is not None:
                    _image = Image(image[1], image[2])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _image

        def get_images(self):
            images = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM images;" )
                for image in cursor:
                    _image = Image(image[1], image[2])
                    images.append((image[0], image[1], _image))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return images


