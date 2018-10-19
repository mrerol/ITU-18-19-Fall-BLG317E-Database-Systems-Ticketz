from flask import render_template, current_app

def home_page():
    return render_template("admin_home_page.html")

def admin_home_page():
    return render_template("admin_home_page.html")


def hotel_page(id):
    return render_template("hotels.html")
