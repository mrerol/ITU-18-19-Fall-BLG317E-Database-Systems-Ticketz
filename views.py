from flask import render_template, current_app, redirect, url_for, request


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

def drivers_page(id):
    return render_template("drivers.html")

def firms_page(id):
    return render_template("firms.html")