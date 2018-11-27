from flask import Flask, render_template, redirect, url_for, request
import views
from base64 import b64encode

from DBOP.tables.image_table import Image
from DBOP.tables.hotel_table import Hotel
from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database

db_hotel = hotel_database()
db_image = image_database()

hotel_db = db_hotel.hotel
image_db = db_image.image

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    return app

app = create_app()

app.secret_key = b'_5#y2L"F4Q8z_^?4c]/'


@app.route('/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    return views.admin_home_page()

@app.route('/search_hotel/<string:text>', methods=['GET', 'POST'])
def search_hotel(text):
    return views.search_hotel_page(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return views.login_page(request)

@app.route('/admin/add_hotel', methods=['GET', 'POST'])
def add_hotel_page():
    if request.method == "GET":
        return views.add_hotel_page()
    else:
        hotel_name = request.form["hotel_name"]
        email = request.form["e_mail"]
        description = request.form["description"]
        city = request.form["city"]
        address = request.form["address"]
        phone = request.form["phone"]
        website = request.form["website"]
        s = request.form["s"]


        hotel_db.add_hotel(Hotel(hotel_name,email,description,city,address,phone,website))

        (temp_id, ) = hotel_db.get_hotel_id(Hotel(hotel_name, email, description, city, address, phone, website))

        uploaded_files = request.form.getlist("file[]")
        for i in range(int(s) + 1):
            temp = "image" + str(i)
            if temp in request.files:
                file = request.files[temp]
                image_db.add_image(Image(temp_id, file.read()))

        return redirect(url_for('admin_home_page'))

@app.route('/admin/edit_hotel/<int:id>', methods=['GET', 'POST'])
def edit_hotel_page(id):
    if request.method == "GET":
        return views.edit_hotel_page(id)
    else:
        hotel_name = request.form["hotel_name"]
        email = request.form["e_mail"]
        description = request.form["description"]
        city = request.form["city"]
        address = request.form["address"]
        phone = request.form["phone"]
        website = request.form["website"]
        hotel_db.update_hotel(id, Hotel(hotel_name,email,description,city,address,phone,website))
        s = request.form["s"]
        uploaded_files = request.form.getlist("file[]")
        print(uploaded_files)
        for i in range(int(s) + 1):
            temp = "image" + str(i)
            if temp in request.files:
                file = request.files[temp]
                image_db.add_image(Image(id, file.read()))

        return redirect(url_for('admin_home_page'))

@app.route('/admin/edit_hotels', methods=['GET', 'POST'])
def edit_hotels_page():
    return views.edit_hotels_page()

@app.route('/admin/delete_hotel/<int:id>')
def delete_hotel(id):
    if(id>6):
        hotel_db.delete_hotel(id)
    return redirect(url_for('edit_hotels_page'))

@app.route('/admin/delete_image/<int:hotel_id>/<int:image_id>')
def delete_image(hotel_id, image_id):
    image_db.delete_image(hotel_id ,image_id)
    return redirect(url_for('edit_hotel_page', id = hotel_id))


@app.route('/hotels/<int:id>', methods=['GET', 'POST'])
def hotel_page(id):
    return views.hotel_page(id)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return views.home_page()

@app.route('/firm/<int:id>', methods=['GET', 'POST'])
def firms_page(id):
    return views.firms_page(id)

@app.route('/firm/driver_list/<int:id>', methods=['GET', 'POST'])
def driver_list_page(id):
    return views.driver_list_page(id)

@app.route('/firm/driver_profile/<int:id>', methods=['GET', 'POST'])
def driver_profile_page(id):
    return views.driver_profile_page(id)

@app.route('/firm/driver_edit/<int:id>', methods=['GET', 'POST'])
def driver_edit_page(id):
    return views.driver_edit_page(id)

@app.route('/firm/add_expedition/<int:id>', methods=['GET', 'POST'])
def add_expedition(id):
    return views.add_expedition(id)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return views.signup_page()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
