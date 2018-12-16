from DBOP.tables.firm_image_table import FirmImage
import psycopg2 as dbapi2
import os

class firm_image_database:
    def __init__(self):
        self.firm_image = self.FirmImage()

    class FirmImage:
        def __init__(self):
            if os.getenv("DATABASE_URL") is None:
                self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
            else:
                self.url = os.getenv("DATABASE_URL")

        def add_image(self, image):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO images_for_firms ( firm_id, file_data) VALUES (%s, %s)",
                    (image.firm_id, image.file_data))
                cursor.close()

        def delete_image(self, firm_id, image_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM images_for_firms WHERE firm_id = %s AND image_id = %s", (firm_id, image_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

        def get_image(self, firm_id, image_id):
            _image = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM images_for_firms WHERE firm_id = %s AND image_id = %s", (firm_id, image_id,))
                image = cursor.fetchone()
                if image is not None:
                    _image = FirmImage(image[1], image[2])
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
                cursor.execute("SELECT * FROM images_for_firms;" )
                for image in cursor:
                    _image = FirmImage(image[1], image[2])
                    images.append((image[0], image[1], _image))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return images

