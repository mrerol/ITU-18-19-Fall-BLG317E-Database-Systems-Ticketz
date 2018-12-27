========================================
Parts Implemented by Muhammed Raşit EROL
========================================

In this section, there are three main tables which are firms, drivers and vehicles; moreover,
images_for_firms table is extra table.
The responsibility of these tables belongs to Muhammed Raşit EROL.
Attributes of tables which are mentioned above can be seen in Figure 1.

Furthermore, ER diagrams of all tables can be seen in
Figure 2, Figure 2, Figure 3, Figure 4 and Figure 5.

firms Table
============

firms table is created for adding and editing expeditions.
Hence, a user is able to see expeditions which are created by firms.
In order organize that operations, firms table is developed as another users table.
However, instead of storing detailed user information, firms table stores information
which are useful for viewing expeditions. Thus, a user can visit firm page which is appeared
in the expedition card. However, main duty of the firms is creating and editing expeditions
which are appears in the user main page. In order the perform that,
email and password attributes are used in the firms table. Other attributes
which are name, phone, city, address, website, description and logo, are used for
getting detailed information when visiting the firm page. The attribute city is used as
foreign key. Also, logo is stored as BLOB type in the database. Moreover,
email and password cannot be NULL because a firm must have these attributes
due to the proper login; furthermore, name and phone cannot be NULL
due to need of at least one contact information and reason for
illogical situation if there is no name for a firm. Also, firm_id is primary key
for firms table and its serially increased by the system. The creation code of
the firms table can be seen below.


.. code-block:: sql

    CREATE TABLE IF NOT EXISTS firms
        (
            firm_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR (20) NOT NULL,
            password VARCHAR (50) NOT NULL,
            email VARCHAR (20) NOT NULL,
            phone VARCHAR (20) NOT NULL,
            city VARCHAR (2),
            address VARCHAR (100),
            website VARCHAR (20),
            description VARCHAR (200),
            logo BYTEA,
            FOREIGN KEY (city) REFERENCES city (code) ON DELETE RESTRICT ON UPDATE CASCADE

        )

All operations of the firms table can be seen below:

Operations
------------

Creating, reading, updating and deleting operations can be performed on the firms table.

The attributes of the firms table correspond the parameters on the Firm class.
Hence, with this approach, it is easy to manage the data which stands for attributes of the firms table.
The Firm class can be seen below:


.. code-block:: python

    class Firm:
        def __init__(self, name, password, email, phone, city, address, website, description, logo=None):
            self.name = name
            self.password = password
            self.email = email
            self.phone = phone
            self.city = city
            self.address = address
            self.website = website
            self.description = description
            self.logo = logo



Also, firm_database class is another class which is used for performing table operations with the methods of the Firm class.
The example add_firm method of Firm class can be seen in the below code. Furthermore, database connection is handled with that class.
Hence, in the firm_database class, all data and methods can be used with the Firm class. Thus, all database operations
are handled with the object oriented approach. The code of firm_database and Firm class can be seen below.

.. code-block:: python

    class firm_database:
        def __init__(self):
            self.firm = self.Firm()

        class Firm:
            def __init__(self):
                if os.getenv("DATABASE_URL") is None:
                    self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
                else:
                    self.url = os.getenv("DATABASE_URL")

            def add_firm(self, firm):
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO firms ( name, password, email, phone, city, address, website, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (firm.name, firm.password, firm.email, firm.phone, firm.city, firm.address, firm.website, firm.description))
                    cursor.close()

The operaitons on the firms table can be seen below.

Insert
^^^^^^^^

The insertion on the firms table can be performed with add_firm and add_firm_with_logo functions of Firm class.
These functions are used for adding new firm to the firm table. The add_firm function takes Firm object and it inserts
the new firm using information of Firm object with given parameter. Also, the add_firm_with_logo functions perform same
operation but with the logo. Hence, with these two functions, new firm can be inserted to the firms table.
These function are called from firm signup page. There is no return value for both two functions.
The code of these functions can be seen in code block below.

.. code-block:: python

        def add_firm(self, firm):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, phone, city, address, website, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (firm.name, firm.password, firm.email, firm.phone, firm.city, firm.address, firm.website, firm.description))
                cursor.close()

        def add_firm_with_logo(self, firm_with_logo):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO firms ( name, password, email, phone, city, address, website, description, logo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (firm_with_logo.name, firm_with_logo.password, firm_with_logo.email, firm_with_logo.phone, firm_with_logo.city, firm_with_logo.address, firm_with_logo.website,firm_with_logo.description, firm_with_logo.logo))
                cursor.close()


Read
^^^^^^^^

The read operation on the firms table can be performed with get_firm and get_firms functions of Firm class.
These functions are used for reading existing firm from the firm table. The get_firm function takes firm_id as parameter and
returns corresponding firm from the firm table. However, the get_firms function does not take parameter and returns
all firms from the firm table. The returned values for both functions are Firm class objects.
They used in the application when firm attributes are desired.
These functions are called from firm list page in admin page.
The code of these functions can be seen in code block below.

.. code-block:: python

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


Furthermore, there are two more functions which is used for read operations also.
The get_firm_id function takes parameter as Firm object and returns the corresponding firm_id for that.
Also, the get_firm_id_login function takes parameter as email and password and returns the corresponding firm_id for login system.
The get_firm_id_login function is used for validation in the firm login page.
The existence of the firm is checked when a firm want to login.
These functions are called from firm list page in admin page.
The code of these functions can be seen in code block below.


.. code-block:: python

        def get_firm_id(self, firm):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM firms WHERE name = %s AND password = %s AND email = %s AND phone= %s  AND city = %s AND address = %s AND website = %s AND description = %s",
                    (firm.name, firm.password, firm.email, firm.phone, firm.city, firm.address, firm.website, firm.description))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def get_firm_id_login(self, email, password):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM firms WHERE email = %s AND password = %s ",
                    (email, password))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

Update
^^^^^^^^
The update operation on the firms table can be performed with update_firm and update_firm_with_logo functions of Firm class.
These functions are used for updating existing firm from the firm table.
The update_firm function takes two parameters which are firm_id and Firm class object, and update the firm with new coming values.
Also, update_firm_with_logo performs same operations but with the logo.
Hence, with these two functions, a firm can be updated at the firms table. These functions are called from firm edit page.
There is no return value for both two functions. The code of these functions can be seen in code block below.

.. code-block:: python

        def update_firm(self, firm_id, firm):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE firms SET name = %s, password = %s, email = %s, phone = %s, city = %s, address = %s, website = %s, description = %s WHERE firm_id = %s """, (firm.name, firm.password, firm.email,firm.phone, firm.city, firm.address, firm.website, firm.description, firm_id))
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
                cursor.execute("""UPDATE firms SET name = %s, password = %s, email = %s, phone = %s, city = %s, address = %s, website = %s, description = %s, logo = %s WHERE firm_id = %s """, (firm.name, firm.password, firm.email,firm.phone, firm.city, firm.address, firm.website, firm.description, firm.logo, firm_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()


Delete
^^^^^^^^

The delete operation on the firms table can be performed with delete_firm and delete_firm_logo functions of Firm class.
These functions are used for deleting existing firm from the firm table and deleting of firm’s logo.
The delete_firm function takes parameter as firm_id and deletes the corresponding firm from the firm table.
Also, the delete_firm_logo function takes parameter as firm_id and deletes the logo of corresponding firm from the firm table.
Hence, with these two functions, a firm or firm logo can be delete from the firms table.
These functions are called from firm list page. There is no return value for both two functions.
The code of these functions can be seen in code block below.

.. code-block:: python

        def delete_firm(self, firm_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM firms WHERE (firm_id = %s) ", (firm_id,))
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

Search
^^^^^^^^
The search operation on the firms table can be performed with search function of Firm class.
This functions are used for searching existing firm on the firm table.
That functions takes parameter as text and returns the corresponding firm from the firms table.
The text parameter is searched on all attributes of the firm table except the password.
If there is attributes which contains the text parameter then the corresponding firm is returned from function.
Hence, with that function a text can be searched on the firms table. This functions are called from the function which is called from navbar in the firm pages.
The code of this function can be seen in code block below.

.. code-block:: python

        def search(self, text):
            firms = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM firms WHERE (name like %s)  or (email like %s) or (city like %s) or (address like %s)  or (phone like %s) or (website like %s) or (description like %s) or (logo like %s)      ;", (to_search, to_search, to_search, to_search, to_search, to_search,to_search,to_search))
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


Related Systems
------------------

There are three system in this section, which provide better workflow for the application. They are listed below.

Signup
^^^^^^^^

There is a signup system for firms, which is different than user signup system.
The signup system is used adding new firms to the application.
This is performed with the insert operation of the firms table.
After validation controls, a firm is added to the system as a kind of user.
If validation is not correct then related error pages are returned.
In the signup system, also password is stored after hashing.
The code of signup function can be seen in code block below.

.. code-block:: python

    def firm_signup(request):
        error = None
        if request.method == "GET":
            cities = city_db.get_all_city()
            return render_template("firm/signup.html", error=error, cities=cities)

        elif request.method == "POST":

            firm_name = request.form["firm_name"]
            e_mail = request.form["e_mail"]
            phone = request.form["phone"]
            description = request.form["description"]
            city = request.form["city"]
            address = request.form["address"]
            website = request.form["website"]

            db_password = request.form['password']+salt
            h = hashlib.md5(db_password.encode())

            if "logo" in request.files:
                logo = request.files["logo"]

                firm_db.add_firm_with_logo(
                    Firm(firm_name, h.hexdigest(), e_mail, phone, city, address, website, description, logo.read()))
            else:
                firm_db.add_firm(Firm(firm_name, h.hexdigest(), e_mail, phone, city, address, website, description, None))

            s = request.form["s"]

            (temp_id,) = firm_db.get_firm_id(
                Firm(firm_name, h.hexdigest(), e_mail, phone, city, address, website, description, None))

            #uploaded_files = request.form.getlist("file[]")
            for i in range(int(s) + 1):
                temp = "image" + str(i)
                if temp in request.files:
                    file = request.files[temp]
                    firm_image_db.add_image(FirmImage(temp_id, file.read()))

            return redirect(url_for('firm_login'))
        else:
            return render_template("403_un_authorized.html")

Moreover, some of the validations which are related to quality of input.
This validation is performed with the JavaScript code.
The code of validation of signup function with JavaScript can be seen in code block below.

.. code-block:: javascript

    function add()
    {

        var $captcha = $( '#recaptcha' ),
            response = grecaptcha.getResponse();

        if (response.length === 0) {
            $( '.msg-error').text( "reCAPTCHA is mandatory" );
            if( !$captcha.hasClass( "error" ) ){
                $captcha.addClass( "error" );
                return false;
            }
        }
        else {
            $( '.msg-error' ).text('');
            $captcha.removeClass( "error" );
        }


        let fill = true;
        let value_length = true;

        if($('#firm_name').val().length < 5 || $('#firm_name').val().length > 20 ){
            document.getElementById("firm_name").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("firm_name").style.borderColor = "green";

        if (($('#e_mail').val().length < 5 || $('#e_mail').val().length > 20 )){
            document.getElementById("e_mail").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("e_mail").style.borderColor = "green";

        if (($('#password').val().length < 5 || $('#password').val().length > 20 )){
            document.getElementById("password").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("password").style.borderColor = "green";

        if (($('#phone').val().length < 5 || $('#phone').val().length > 20 )){
            document.getElementById("phone").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("phone").style.borderColor = "green";

        if(fill && value_length){
            $('#s').val(image_count)
            document.getElementById("add_firm").submit()
        }
        else{
                $(".message-box-danger-length").toggle(750, function () {
                    setTimeout(function () {
                        $(".message-box-danger-length").toggle(750);
                    }, 2500);
                });

       }

    }

Login
^^^^^^^^

There is a login system for firms, which is similar to user login system.
The firm login system is used for entering the system with a firm nor regular user.
This is performed with the read operation of the firms table.
After validation controls, a firm can login to the system.
One the validation control is comparing hashed password with the coming hashed password from database.
If validation is not correct then related error pages are returned.
The code of login function can be seen in code block below.

.. code-block:: python

    def firm_login(request):
        if request.method == "POST":
            email = request.form['e_mail']
            db_password = request.form['password']+salt
            h = hashlib.md5(db_password.encode())

            try:
                temp = firm_db.get_firm_id_login(email, h.hexdigest())

                if temp is not None:
                    (firm_id,) = temp
                    print(firm_id)
                    session.permanent = True
                    session['firm_id'] = firm_id
                    return redirect(url_for('firm_page', id=firm_id))
                else:
                    return render_template("firm/login.html", error = "Wrong e mail or password")
            except:
                return render_template("firm/login.html", error="Something wents wrong please try again")


        elif request.method == "GET":
            return render_template("firm/login.html", error = None)
        else:
            return render_template("404_not_found.html")


Moreover, some of the validations which are related to quality of input.
This validation is performed with the JavaScript code.
The code of validation of login function with JavaScript can be seen in code block below.

.. code-block:: javascript

    function login()
    {
        var $captcha = $( '#recaptcha' ),
            response = grecaptcha.getResponse();

        if (response.length === 0) {
            $( '.msg-error').text( "reCAPTCHA is mandatory" );
            if( !$captcha.hasClass( "error" ) ){
                $captcha.addClass( "error" );
                return false;
            }
        }
        else {
            $( '.msg-error' ).text('');
            $captcha.removeClass( "error" );
        }


        let fill = true;
        let value_length = true;

        if($('#e_mail').val().length < 5 || $('#e_mail').val().length > 20 ){
            document.getElementById("e_mail").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("e_mail").style.borderColor = "green";

        if (($('#password').val().length < 5 || $('#password').val().length > 20 )){
            document.getElementById("password").style.borderColor = "red";
            value_length = false;
        }
        else
            document.getElementById("password").style.borderColor = "green";


        if(fill && value_length){
            document.getElementById("login_firm").submit()
        }
        else{
                $(".message-box-danger-length").toggle(750, function () {
                    setTimeout(function () {
                        $(".message-box-danger-length").toggle(750);
                    }, 2500);
                });

       }

    }


drivers Table
==============

deneme

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS drivers
        (
            driver_id SERIAL NOT NULL PRIMARY KEY,
            name VARCHAR (20) NOT NULL,
            email VARCHAR (20) NOT NULL,
            gender VARCHAR (20),
            city VARCHAR (2),
            address VARCHAR (200),
            phone VARCHAR (20) NOT NULL,
            firm_id INT,
            FOREIGN KEY (city) REFERENCES city (code) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (firm_id) REFERENCES firms (firm_id) ON DELETE CASCADE ON UPDATE CASCADE
        )

All operations of the drivers table can be seen below:

Operations
------------

Creating, reading, updating and deleting operations can be performed on the drivers table.

The attributes of the drivers table correspond the parameters on the Driver class.
Hence, with this approach, it is easy to manage the data which stands for attributes of the drivers table.
The Driver class can be seen below:

.. code-block:: python

    class Driver:
        def __init__(self, name, email, gender, city, address, phone, firm_id ):
            self.name = name
            self.email = email
            self.gender = gender
            self.city = city
            self.address = address
            self.phone = phone
            self.firm_id = firm_id




Also, driver_database class is another class which is used for performing table operations with the methods of the Driver class.
The example add_driver method of Driver class can be seen in the below code.
Furthermore, database connection is handled with that class.
Hence, in the driver_database class, all data and methods can be used with the Driver class. Thus, all database operations
are handled with the object oriented approach. The code of driver_database and Driver class can be seen below.

.. code-block:: python

    class driver_database:
        def __init__(self):
            self.driver = self.Driver()

        class Driver:
            def __init__(self):
                if os.getenv("DATABASE_URL") is None:
                    self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
                else:
                    self.url = os.getenv("DATABASE_URL")

            def add_driver(self, driver):
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO drivers ( name, email, gender, city, address, phone, firm_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone, driver.firm_id))
                    cursor.close()

The operations on the drivers table can be seen below.

Insert
^^^^^^^^

The insertion on the firms table can be performed with add_firm and add_firm_with_logo functions of Firm class.
These functions are used for adding new firm to the firm table. The add_firm function takes Firm object and it inserts
the new firm using information of Firm object with given parameter. Also, the add_firm_with_logo functions perform same
operation but with the logo. Hence, with these two functions, new firm can be inserted to the firms table.
These function are called from firm signup page. There is no return value for both two functions.
The code of these functions can be seen in code block below.

.. code-block:: python

        def add_driver(self, driver):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO drivers ( name, email, gender, city, address, phone, firm_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone, driver.firm_id))
                cursor.close()



Read
^^^^^^^^

The read operation on the firms table can be performed with get_firm and get_firms functions of Firm class.
These functions are used for reading existing firm from the firm table. The get_firm function takes firm_id as parameter and
returns corresponding firm from the firm table. However, the get_firms function does not take parameter and returns
all firms from the firm table. The returned values for both functions are Firm class objects.
They used in the application when firm attributes are desired.
These functions are called from firm list page in admin page.
The code of these functions can be seen in code block below.

.. code-block:: python

       def get_driver(self, driver_id):
            _driver = None
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
                driver = cursor.fetchone()
                if driver is not None:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return _driver

        def get_drivers(self):
            drivers = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers;")
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers

        def get_drivers_for_firms(self, firm_id):
            drivers = []
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE (firm_id = %s)",(firm_id,))
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers

Furthermore, there are two more functions which is used for read operations also.
The get_firm_id function takes parameter as Firm object and returns the corresponding firm_id for that.
Also, the get_firm_id_login function takes parameter as email and password and returns the corresponding firm_id for login system.
The get_firm_id_login function is used for validation in the firm login page.
The existence of the firm is checked when a firm want to login.
These functions are called from firm list page in admin page.
The code of these functions can be seen in code block below.


.. code-block:: python

        def get_driver_id(self, driver):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT driver_id FROM drivers WHERE name = %s AND email = %s AND gender = %s AND city = %s AND address = %s AND phone= %s ",
                    (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone))
                temp_id = cursor.fetchone()
                cursor.close()
                return temp_id

        def get_firm_ids(self, driver_id):
            with dbapi2.connect(self.url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT firm_id FROM drivers WHERE driver_id = %s ", (driver_id,))
                drivers = cursor.fetchall()
                cursor.close()
                return drivers

Update
^^^^^^^^
The update operation on the firms table can be performed with update_firm and update_firm_with_logo functions of Firm class.
These functions are used for updating existing firm from the firm table.
The update_firm function takes two parameters which are firm_id and Firm class object, and update the firm with new coming values.
Also, update_firm_with_logo performs same operations but with the logo.
Hence, with these two functions, a firm can be updated at the firms table. These functions are called from firm edit page.
There is no return value for both two functions. The code of these functions can be seen in code block below.

.. code-block:: python

        def update_driver(self, driver_id, driver):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("""UPDATE drivers SET name = %s, email = %s, gender = %s, city = %s, address = %s, phone = %s, firm_id = %s WHERE driver_id= %s """, (driver.name, driver.email, driver.gender, driver.city, driver.address, driver.phone, driver.firm_id, driver_id))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()



Delete
^^^^^^^^

The delete operation on the firms table can be performed with delete_firm and delete_firm_logo functions of Firm class.
These functions are used for deleting existing firm from the firm table and deleting of firm’s logo.
The delete_firm function takes parameter as firm_id and deletes the corresponding firm from the firm table.
Also, the delete_firm_logo function takes parameter as firm_id and deletes the logo of corresponding firm from the firm table.
Hence, with these two functions, a firm or firm logo can be delete from the firms table.
These functions are called from firm list page. There is no return value for both two functions.
The code of these functions can be seen in code block below.

.. code-block:: python

        def delete_driver(self, driver_id):
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()

Search
^^^^^^^^
The search operation on the firms table can be performed with search function of Firm class.
This functions are used for searching existing firm on the firm table.
That functions takes parameter as text and returns the corresponding firm from the firms table.
The text parameter is searched on all attributes of the firm table except the password.
If there is attributes which contains the text parameter then the corresponding firm is returned from function.
Hence, with that function a text can be searched on the firms table. This functions are called from the function which is called from navbar in the firm pages.
The code of this function can be seen in code block below.

.. code-block:: python

        def search(self, text, firm_id):
            drivers = []
            to_search = "%" + text + "%"
            try:
                connection = dbapi2.connect(self.url)
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM drivers WHERE ((name like %s)  or (email like %s) or (gender like %s) or (city like %s) or (address like %s)  or (phone like %s) ) and firm_id=%s ;", (to_search, to_search, to_search, to_search, to_search, to_search,firm_id))
                for driver in cursor:
                    _driver = Driver(driver[1], driver[2], driver[3], driver[4], driver[5], driver[6], driver[7])
                    drivers.append((driver[0], _driver))
                connection.commit()
                cursor.close()
            except (Exception, dbapi2.DatabaseError) as error:
                print(error)
            finally:
                if connection is not None:
                    connection.close()
            return drivers


vehicles Table
==============

deneme

.. code-block:: sql

    CREATE TABLE IF NOT EXISTS vehicles
          (
              vehicle_id SERIAL NOT NULL PRIMARY KEY,
              name VARCHAR (20) NOT NULL,
              category VARCHAR (20) NOT NULL,
              model VARCHAR (20) NOT NULL,
              capacity INT NOT NULL,
              production_year INT NOT NULL,
              production_place VARCHAR (20) NOT NULL,
              description VARCHAR (200),
              document BYTEA,
              firm_id INT,
              FOREIGN KEY (firm_id) REFERENCES firms (firm_id)

          )

All operations of the vehicles table can be seen below:

Operations
------------

Creating, reading, updating and deleting operations can be performed on the vehicles table.

The attributes of the vehicles table correspond the parameters on the Vehicle class.
Hence, with this approach, it is easy to manage the data which stands for attributes of the vehicles table.
The Vehicle class can be seen below:

.. code-block:: python

    class Vehicle:
        def __init__(self, name, category, model, capacity, production_year, production_place, description, firm_id, document=None):
            self.name = name
            self.category = category
            self.model = model
            self.capacity = capacity
            self.production_year = production_year
            self.production_place = production_place
            self.description = description
            self.firm_id = firm_id
            self.document = document



Also, vehicle_database class is another class which is used for performing table operations with the methods of the Vehicle class.
The example add_vehicle method of Vehicle class can be seen in the below code.
Furthermore, database connection is handled with that class.
Hence, in the vehicle_database class, all data and methods can be used with the Vehicle class. Thus, all database operations
are handled with the object oriented approach. The code of vehicle_database and Vehicle class can be seen below.

.. code-block:: python

    class vehicle_database:
        def __init__(self):
            self.vehicle = self.Vehicle()

        class Vehicle:
            def __init__(self):
                if os.getenv("DATABASE_URL") is None:
                    self.url = "postgres://itucs:itucspw@localhost:32768/itucsdb"
                else:
                    self.url = os.getenv("DATABASE_URL")

            def add_vehicle(self, vehicle):
                with dbapi2.connect(self.url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(
                        "INSERT INTO vehicles ( name, category, model, capacity, production_year, production_place, description,firm_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (vehicle.name, vehicle.category, vehicle.model, vehicle.capacity, vehicle.production_year, vehicle.production_place, vehicle.description, vehicle.firm_id))
                    cursor.close()

The operations on the vehicles table can be seen below.

Insert
^^^^^^^^

denmee
