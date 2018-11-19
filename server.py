from flask import Flask, render_template, redirect, url_for, request
import views

from tables import Hotel
from dboperations import Database

db = Database()

hotel_db = db.hotel

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    return app

app = create_app()

@app.route('/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    return views.admin_home_page()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return views.login_page(request)

@app.route('/hotels/<int:hotel_id>', methods=['GET', 'POST'])
def home(hotel_id):
    #hotel_ = hotel_db.get_hotel(hotel_id)
    #print(hotel_)
    return render_template("hotels.html",)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return views.home_page()

@app.route('/firms/<int:id>', methods=['GET', 'POST'])
def firms_page():
    return views.firms_page()

@app.route('/drivers/<int:id>', methods=['GET', 'POST'])
def drivers_page():
    return views.drivers_page()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
