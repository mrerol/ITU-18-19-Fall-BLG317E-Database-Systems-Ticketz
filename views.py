from flask import render_template, current_app, redirect, url_for, request




def home_page():
    return render_template("admin_home_page.html")

def admin_home_page():
    return render_template("admin_home_page.html")

def login_page(request):
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin_home_page'))
    return render_template('login.html')

def hotel_page(id):
    return render_template("hotels.html")

def drivers_page(id):
    return render_template("drivers.html")

def firms_page(id):
    return render_template("firms.html")