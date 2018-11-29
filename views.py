from flask import render_template, redirect, url_for, request, session
from dao.user_dao import UserDao
from psycopg2 import IntegrityError
import sys
from base64 import b64encode

from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database

db_hotel = hotel_database()
db_image = image_database()

hotel_db = db_hotel.hotel
image_db = db_image.image

userop = UserDao()

def home_page():
    hotels = hotel_db.get_hotels()

    for (id , hotel) in hotels:
        if hotel.logo is not None:
            temp = b64encode(hotel.logo).decode("utf-8")
            hotel.logo = temp

    return render_template("admin_home_page.html", hotels = hotels)



def admin_home_page():
    hotels = hotel_db.get_hotels()

    for (id, hotel) in hotels:
        if hotel.logo is not None:
            temp = b64encode(hotel.logo).decode("utf-8")
            hotel.logo = temp

    return render_template("admin_home_page.html", hotels=hotels)


def search_hotel_page(text):
    #if 'user_id' in session:
    hotels = hotel_db.search(text)
    return render_template("admin_home_page.html", hotels = reversed(hotels))
    #else:
    #    return redirect(url_for('404_not_found'))


def add_hotel_page():
    return render_template("add_hotel.html")

def edit_hotel_page(id):
    temp_hotel = hotel_db.get_hotel(id)
    if temp_hotel is None:
        return render_template("404_not_found.html")
    else:
        tmp = image_db.get_images()
        if temp_hotel.logo is not None:
            temp_hotel.logo = b64encode(temp_hotel.logo).decode("utf-8")
        images = []
        for (h_id, image_id,  im) in tmp:
            if id == h_id:
                image = b64encode(im.file_data).decode("utf-8")
                images.append((image_id, image) )
        return render_template("edit_hotel.html", hotel = temp_hotel, images = images, hotel_id = id)

def edit_hotels_page():
    #if 'user_id' in session:
    hotels = hotel_db.get_hotels()
        #print(hotels)
    return render_template("edit_hotels.html", hotels = reversed(hotels))
    #else:
    #    return redirect(url_for('404_not_found'))


def login_page(request):
    error = None
    if request.method == 'POST':
        try:
            user_id = userop.get_user_id(request.form['username'],request.form['password'])
            print("userid ",user_id)
            if user_id is not None:
                session['user_id'] = user_id
                return redirect(url_for('admin_home_page'))
            else:
                # TODO user not found
                error = "invalid credentials"
                #return render_template("404_not_found.html")# TODO add 403
        except:
            print("login generic errorrrrrrr",sys.exc_info())
            error = "error"
            # TODO pop up error message
    return render_template('login.html',error = error)

def hotel_page(id):
    temp_hotel = hotel_db.get_hotel(id)
    if temp_hotel is None:
        return render_template("404_not_found.html")
    else:
        toSend = []
        images = image_db.get_images()
        if temp_hotel.logo is not None:
            temp_hotel.logo = b64encode(temp_hotel.logo).decode("utf-8")
        for ( temp_id, trash, image) in images:
            if temp_id is id:
                toSend.append(b64encode(image.file_data).decode("utf-8"))
        return render_template("hotels.html", hotel = temp_hotel , images = toSend)


def driver_list_page(id):
    return render_template("driver/driver_list.html")

def driver_profile_page(id):
    return render_template("driver/driver_profile.html")

def driver_edit_page(id):
    return render_template("driver/driver_edit.html")

def firms_page(id):
    return render_template("firm/firm.html")

def add_expedition(id):
    return render_template("firm/firm.html")

def signup_page():
    error = None
    try: 
        userid = userop.add_user(request.form['username'],request.form['name'],request.form['surname'],
                                request.form['gender'],request.form['mail'],request.form['password'],
                                request.form['phone'],request.form['address'])
        print("userid: ",userid)
        session['user_id'] = userid
        return redirect(url_for('login'))
    except IntegrityError:
        print("duplicate entry")
        error = "duplicate entry"
        pass # TODO show error pop up for already existing user
    except:
        print("generic errorrrrrrr",sys.exc_info())
        pass # TODO show generic pop up error
    return render_template("signup.html",error = error)

