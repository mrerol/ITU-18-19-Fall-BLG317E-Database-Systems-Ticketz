from flask import render_template, current_app, redirect, url_for, request, session
from dao.user_dao import UserDao
from psycopg2 import IntegrityError
import sys

from tables import Hotel
from dboperations import Database

db = Database()

hotel_db = db.hotel
userop = UserDao()

def home_page():
    hotels = hotel_db.get_hotels()
    return render_template("admin_home_page.html", hotels = reversed(hotels))

def admin_home_page():
    #if 'user_id' in session:
    hotels = hotel_db.get_hotels()
        #print(hotels)
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
        return render_template("edit_hotel.html", hotel = temp_hotel)

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

