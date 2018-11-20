from flask import render_template, current_app, redirect, url_for, request
from dao.user_dao import UserDao
from psycopg2 import IntegrityError
import sys

from tables import Hotel
from dboperations import Database

db = Database()

hotel_db = db.hotel


def home_page():
    hotels = hotel_db.get_hotels()
    return render_template("admin_home_page.html", hotels = sorted(hotels))

def admin_home_page():
    hotels = hotel_db.get_hotels()
    #print(hotels)
    return render_template("admin_home_page.html", hotels = sorted(hotels))

def login_page(request):
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin_home_page'))
    return render_template('login.html')

def hotel_page(id):
    temp_hotel = hotel_db.get_hotel(id)
    return render_template("hotels.html", hotel = temp_hotel)

def driver_list_page(id):
    return render_template("driver/driver_list.html")

def driver_profile_page(id):
    return render_template("driver/driver_profile.html")

def driver_edit_page(id):
    return render_template("driver/driver_edit.html")

def firms_page(id):
    return render_template("firms.html")

def signup_page():
    userop = UserDao()
    try: 
        userid = userop.add_user(request.form['username'],request.form['name'],request.form['surname'],
                                request.form['gender'],request.form['mail'],request.form['password'],
                                request.form['phone'],request.form['address'])
        print("userid: ",userid)
        # TODO redirect login page
    except IntegrityError:
        print("duplicate entry")
        pass # TODO show error pop up for already existing user
    except:
        print("generic errorrrrrrr",sys.exc_info())
        pass # TODO show generic pop up error
    return render_template("signup.html")

