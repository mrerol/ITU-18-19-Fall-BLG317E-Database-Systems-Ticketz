from flask import render_template, redirect, url_for, request, session
from dao.user_dao import UserDao
from psycopg2 import IntegrityError
import sys
from base64 import b64encode
from datetime import datetime
import hashlib

from DBOP.tables.firms_table import Firm
from DBOP.tables.firm_image_table import FirmImage
from DBOP.tables.drivers_table import Driver
from DBOP.tables.vehicles_table import Vehicle
from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database
from DBOP.firm_image_db import firm_image_database
from DBOP.seat_db import seat_database
from DBOP.ticket_db import ticket_database
from DBOP.firms_db import firm_database
from DBOP.vehicles_db import vehicle_database
from DBOP.drivers_db import driver_database
from DBOP.expedition_db import expedition_database
from dao.city_dao import CityDao
from dao.terminal_dao import TerminalDao
from dao.sale_dao import SaleDao


from DBOP.tables.expedition_table import Expedition
from DBOP.tables.ticket_table import Ticket

db_firm_image = firm_image_database()
db_hotel = hotel_database()
db_image = image_database()
db_firm = firm_database()
db_vehicle = vehicle_database()
db_driver = driver_database()
db_expedition = expedition_database()
db_seat = seat_database()
db_ticket = ticket_database()

hotel_db = db_hotel.hotel
image_db = db_image.image
firm_db = db_firm.firm
firm_image_db = db_firm_image.firm_image
vehicle_db = db_vehicle.vehicle
driver_db = db_driver.driver
expedition_db = db_expedition.expedition
seat_db = db_seat.seat
ticket_db = db_ticket.ticket

userop = UserDao()
city_db = CityDao()
terminalop = TerminalDao()
sale_db = SaleDao()


salt = "3re"

today = datetime.today()

str_today = str(today.month) + '/' + str(today.day) + '/' + str(today.year)

def dayCompare( toCompare):
    t0 = str_today.split('/', 3)
    t1 = toCompare.split('/', 3)
    if t0[2] > t1[2]:
        return False
    elif t0[2] == t1[2]:
        if t0[1] > t1[1]:
            return False
        elif t0[1] == t1[1]:
            if t0[0] >= t1[0]:
                return False
            else:
                return True
        else:
            return True
    else:
        return True



def home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    firms = firm_db.get_firms()
    expeditions = expedition_db.get_all_valid_expeditions()
    cities = city_db.get_all_city();
    for (expedition_id, temp_expedition) in expeditions:
        temp_expedition.expedition_id = expedition_id
        firm = firm_db.get_firm(temp_expedition.firm_id)
        print(firm)

        firm.firm_id = temp_expedition.firm_id
        temp_expedition.firm = firm

        from_city = city_db.get_city(temp_expedition.from_)
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        sale = sale_db.get_sale_price(temp_expedition.firm_id, user_id)
        price = temp_expedition.price
        temp_expedition.has_sale = False
        if sale is not None:
            price -= sale[0]
            temp_expedition.has_sale = True
        temp_expedition.price = price
        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(expedition_id)
        else:
            temp_expedition.document_link = None


    return render_template("home_page.html", user=user, expeditions = expeditions, firms = firms,  cities = cities)


def filtered_home_page():
    to_city = None
    to_ter = None
    from_city = None
    from_ter = None
    firm_id = None
    date = None
    max_price = None
    if request.form.getlist('to'):
        to_city = request.form["to"]
    if request.form.getlist("to_ter"):
        to_ter = request.form["to_ter"]
    if request.form.getlist("from"):
        from_city = request.form["from"]
    if request.form.getlist("from_ter"):
        from_ter = request.form["from_ter"]
    if request.form.getlist("firm_id"):
        firm_id = request.form["firm_id"]
    if request.form.getlist("date"):
        date = request.form["date"]
    if request.form.getlist("max_price"):
        max_price = request.form["max_price"]


    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    firms = firm_db.get_firms()

    print(to_ter)
    expeditions = expedition_db.get_filtered_expeditions(to_city, to_ter, from_city, from_ter, firm_id, date, max_price)
    cities = city_db.get_all_city();
    for (expedition_id, temp_expedition) in expeditions:
        temp_expedition.expedition_id = expedition_id
        firm = firm_db.get_firm(temp_expedition.firm_id)

        firm.firm_id = temp_expedition.firm_id
        temp_expedition.firm = firm

        from_city = city_db.get_city(temp_expedition.from_)
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name

        sale = sale_db.get_sale_price(temp_expedition.firm_id, user_id)
        price = temp_expedition.price
        temp_expedition.has_sale = False
        if sale is not None:
            price -= sale[0]
            temp_expedition.has_sale = True
        temp_expedition.price = price

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(expedition_id)
        else:
            temp_expedition.document_link = None


    return render_template("home_page.html", user=user, expeditions = expeditions, cities = cities, firms = firms)




def admin_home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)

    return render_template("admin/admin_home_page.html", user = user)

def my_profile():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)

    return render_template("user/my_profile.html", user = user)



def hotels_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    hotels = hotel_db.get_hotels()
    for (id , hotel) in hotels:
        if hotel.logo is not None:
            temp = b64encode(hotel.logo).decode("utf-8")
            hotel.logo = temp
    return render_template("hotel/hotel_list.html", hotels = (hotels), user = user)

def search_hotel_page(text):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    hotels = hotel_db.search(text)
    for (id , hotel) in hotels:
        if hotel.logo is not None:
            temp = b64encode(hotel.logo).decode("utf-8")
            hotel.logo = temp
    return render_template("hotel/hotel_list.html", hotels = (hotels), user = user)

def search_ticket_page(text):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    tickets = ticket_db.search(text)
    print(tickets)
    for (id, ticket) in tickets:
        temp_expedition = expedition_db.get_expedition(ticket.expedition_id)
        firm = firm_db.get_firm(temp_expedition.firm_id)
        firm.firm_id = id
        from_city = city_db.get_city(temp_expedition.from_)
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name
        if dayCompare(temp_expedition.date) and ticket.is_cancelable:
            ticket.is_cancelable = True
            ticket.editable = True
        elif dayCompare(temp_expedition.date):
            ticket.editable = True
        else:
            ticket.is_cancelable = False
            ticket.editable = False



        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(id)

        else:
            temp_expedition.document_link = None

        ticket.expedition = temp_expedition
        ticket.firm = firm
        ticket.ticket_id = id

    return render_template("ticket/ticket_search.html", user=user, tickets=tickets)


def search_expedition_page(text):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    expeditions = expedition_db.search(text)

    for (expedition_id, temp_expedition) in expeditions:
        temp_expedition.expedition_id = expedition_id
        firm = firm_db.get_firm(temp_expedition.firm_id)

        firm.firm_id = temp_expedition.firm_id
        temp_expedition.firm = firm

        from_city = city_db.get_city(temp_expedition.from_)
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name

        sale = sale_db.get_sale_price(temp_expedition.firm_id, user_id)
        price = temp_expedition.price
        temp_expedition.has_sale = False
        if sale is not None:
            price -= sale[0]
            temp_expedition.has_sale = True
        temp_expedition.price = price

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(expedition_id)
        else:
            temp_expedition.document_link = None


    return render_template("firm/expedition_search.html", user=user, expeditions = expeditions)

def add_hotel_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    cities = city_db.get_all_city()
    return render_template("hotel/add_hotel.html", cities = cities, user = user)

def edit_hotel_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    temp_hotel = hotel_db.get_hotel(id)
    hotel_city = city_db.get_city(temp_hotel.city)
    (city_code, hotel_city_name) = hotel_city
    if temp_hotel is None:
        return render_template("404_not_found.html")
    else:
        cities = city_db.get_all_city()
        tmp = image_db.get_images()
        if temp_hotel.logo is not None:
            temp_hotel.logo = b64encode(temp_hotel.logo).decode("utf-8")
        images = []
        for (h_id, image_id,  im) in tmp:
            if id == h_id:
                image = b64encode(im.file_data).decode("utf-8")
                images.append((image_id, image) )
        return render_template("hotel/edit_hotel.html", hotel = temp_hotel, images = images, hotel_id = id, cities = cities, code = city_code, hotel_city = hotel_city_name, user = user)

def edit_hotels_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    cities = hotel_db.get_hotels_with_cities()
    hotels = hotel_db.get_hotels()
    return render_template("hotel/edit_hotels.html", hotels = reversed(hotels), cities = cities, user = user)

def edit_expeditions_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    expeditions = expedition_db.get_all_expeditions()
    return render_template("admin/expedition_list.html", user = user, expeditions=expeditions)

def login_page(request):
    error = ""
    if request.method == 'POST':
        try:
            db_password = request.form['password']+salt
            h = hashlib.md5(db_password.encode())
            user_id = userop.get_user_id(request.form['username'],h.hexdigest())
            if user_id is not None:
                session['user_id'] = user_id
                return redirect(url_for('home_page'))
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
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
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
        city = city_db.get_city(temp_hotel.city)
        (code, city_name) = city
        return render_template("hotel/hotels.html", hotel = temp_hotel, images = toSend, city_name = city_name, user = user)

def search_firm_page(search_for):

    firms = firm_db.search(search_for)
    user_id = session.get('user_id')
    user = userop.get_user(user_id)

    for (id, firm) in firms:
        if firm.logo is not None:
            temp = b64encode(firm.logo).decode("utf-8")
            firm.logo = temp


    for (id, firm) in firms:
        firm.city_name = city_db.get_city(firm.city)[1]

    return render_template("firm/firm_list.html", firms=(firms), user=user)

def add_driver_page(request):
    #session.permanent = True
    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    if request.method == "GET":
        cities = city_db.get_all_city()
        return render_template("driver/add_driver.html", cities=cities )
    elif request.method == "POST":
        driver_name = request.form["driver_name"]
        e_mail = request.form["e_mail"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        city = request.form["city"]
        address = request.form["address"]

        driver_db.add_driver(Driver(driver_name, e_mail, gender, city, address, phone, firm_id))

        return redirect(url_for('driver_list_page', id=firm_id))

    else:
        return render_template("403_un_authorized.html")

def driver_list_page(id):
    #session.permanent = True

    drivers = driver_db.get_drivers_for_firms(id);
    for (id, driver) in drivers:
        driver.city_name = city_db.get_city(driver.city)[1]

    return render_template("driver/driver_list.html",drivers=drivers)

def search_driver_page(search_for):

    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    drivers = driver_db.search(search_for,firm_id)

    return render_template("driver/driver_list.html", drivers = drivers)

def driver_edit_page(request,driver_id):

    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    driver = driver_db.get_driver(driver_id)
    city=city_db.get_city(driver.city)
    (thresh,temp_city)=city
    cities = city_db.get_all_city()

    if request.method == "GET":

        if driver is None:
            return render_template("403_un_authorized.html")

        temp=driver_db.get_firm_ids(driver_id)
        flag=0
        for item in temp:
          (temp_item,)=item
          #print(temp_item)
          #print(driver_id)
          if temp_item == firm_id:
                  flag=1

        if flag != 1:
            return render_template("403_un_authorized.html")
        return render_template("driver/driver_edit.html",driver=driver, city=temp_city, cities=cities)

    elif request.method == "POST":

        if driver is None:
            return render_template("403_un_authorized.html")

        driver_name = request.form["driver_name"]
        e_mail = request.form["e_mail"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        city = request.form["city"]
        address = request.form["address"]

        driver_db.update_driver(driver_id, Driver(driver_name, e_mail, gender, city, address, phone, firm_id))

        return redirect(url_for('driver_list_page', id=firm_id))
    else:
        return render_template("403_un_authorized.html")

def driver_delete_page(driver_id):
    temp_id = session.get('firm_id')

    if temp_id is None:
        return render_template("403_un_authorized.html")

    driver_db.delete_driver(driver_id)
    return redirect(url_for('driver_list_page',id=temp_id))

def add_vehicle_page(request):
    #session.permanent = True
    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    if request.method == "GET":
        return render_template("vehicle/add_vehicle.html")

    elif request.method == "POST":

        vehicle_name = request.form["vehicle_name"]
        category = request.form["category"]
        model = request.form["model"]
        capacity = request.form["capacity"]
        production_year = request.form["production_year"]
        production_place = request.form["production_place"]
        description = request.form["description"]

        if "document" in request.files:
            document = request.files["document"]
            vehicle_db.add_vehicle_with_document(Vehicle(vehicle_name,category,model,capacity,production_year,production_place,description,firm_id,document.read()))

        else:
            vehicle_db.add_vehicle(Vehicle(vehicle_name, category, model, capacity, production_year, production_place, description, firm_id, None))

        return redirect(url_for('vehicle_list_page', id=firm_id))

    else:
        return render_template("403_un_authorized.html")

def vehicle_list_page(id):
    #session.permanent = True
    vehicles = vehicle_db.get_vehicles_for_firms(id);
    #print(vehicles)
    return render_template("vehicle/vehicle_list.html", vehicles=vehicles)

def search_vehicle_page(search_for):

    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    vehicles = vehicle_db.search(search_for,firm_id)

    return render_template("vehicle/vehicle_list.html", vehicles = vehicles)

def vehicle_edit_page(request, vehicle_id):

    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("403_un_authorized.html")

    vehicle = vehicle_db.get_vehicle(vehicle_id)

    if request.method == "GET":

        if vehicle is None:
            return render_template("403_un_authorized.html")

        temp = vehicle_db.get_firm_ids(vehicle_id)
        flag=0
        for item in temp:
            (temp_item,)=item
            if temp_item == firm_id:
                    flag=1

        if flag != 1:
            return render_template("403_un_authorized.html")

        if vehicle.document is not None:
            vehicle.document_link = "/vehicle/document/" + str(vehicle_id)
        else:
            vehicle.document_link = None

        return render_template("vehicle/vehicle_edit.html",vehicle=vehicle,vehicle_id=vehicle_id)

    elif request.method == "POST":

        if vehicle is None:
            return render_template("403_un_authorized.html")

        vehicle_name = request.form["vehicle_name"]
        category = request.form["category"]
        model = request.form["model"]
        capacity = request.form["capacity"]
        production_year = request.form["production_year"]
        production_place = request.form["production_place"]
        description = request.form["description"]

        if "document" in request.files:
            document = request.files["document"]

            vehicle_db.update_vehicle_with_document(vehicle_id, Vehicle(vehicle_name, category, model, capacity, production_year, production_place, description,firm_id,document.read()))
        else:
            vehicle_db.update_vehicle(vehicle_id, Vehicle(vehicle_name, category, model, capacity, production_year,
                                                          production_place, description, firm_id))

        return redirect(url_for('vehicle_list_page', id=firm_id))
    else:
        return render_template("403_un_authorized.html")

def vehicle_delete_page(vehicle_id):

    temp_id = session.get('firm_id')

    if temp_id is None:
        return render_template("403_un_authorized.html")

    vehicle_db.delete_vehicle(vehicle_id)
    return redirect(url_for('vehicle_list_page',id=temp_id))

def delete_firm_page(firm_id):

    firm_db.delete_firm(firm_id)

    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    firms = firm_db.get_firms()

    for (id, firm) in firms:
        if firm.logo is not None:
            temp = b64encode(firm.logo).decode("utf-8")
            firm.logo = temp

    cities = city_db.get_all_city()
    return render_template("firm/firm_list.html", firms=(firms), user=user, cities=cities)

def firm_page(id):
    firm_id = session.get('firm_id')
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if firm_id is None and user is None:
        return render_template("403_un_authorized.html")
    else:

        firm = firm_db.get_firm(id)
        logged_firm = firm_db.get_firm(firm_id)

        toSend = []
        images = firm_image_db.get_images()

        if firm.logo is not None:
            firm.logo = b64encode(firm.logo).decode("utf-8")

        for ( temp_id, trash, image) in images:
            if temp_id is id:
                toSend.append(b64encode(image.file_data).decode("utf-8"))

        city = city_db.get_city(firm.city)
        (code, city_name) = city
        return render_template("firm/firm.html", user = user, firm=firm, logged_firm=logged_firm, city_name = city_name, firm_id=id, images=toSend)


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

def firm_logout():
    session.pop('firm_id')
    return redirect(url_for('firm_login'))

def firm_list_page(request):
    if request.method == "GET":
        user_id = session.get('user_id')
        user = userop.get_user(user_id)
        firms = firm_db.get_firms()

        for (id, firm) in firms:
            if firm.logo is not None:
                temp = b64encode(firm.logo).decode("utf-8")
                firm.logo = temp

        firms = firm_db.get_firms()
        for (id, firm) in firms:
            firm.city_name = city_db.get_city(firm.city)[1]

        return render_template("firm/firm_list.html", firms=(firms), user=user)

    return render_template("firm/firm_list.html", firms=firms)

def edit_firm_page(request):

    firm_id = session.get('firm_id')
    if firm_id is None:
        return render_template("403_un_authorized.html")

    if request.method == "GET":

        firm=firm_db.get_firm(firm_id)
        city = city_db.get_city(firm.city)
        (code, city_name) = city
        cities = city_db.get_all_city()
        tmp = firm_image_db.get_images()

        if firm.logo is not None:
            firm.logo = b64encode(firm.logo).decode("utf-8")

        images = []
        for (h_id, image_id,  im) in tmp:
            if firm_id == h_id:
                image = b64encode(im.file_data).decode("utf-8")
                images.append((image_id, image) )

        return render_template("firm/edit_firmpage.html",firm=firm, cities = cities, city_name=city_name, images=images,firm_id=firm_id)

    elif request.method == "POST":
        firm_name = request.form["firm_name"]
        password = request.form["password"]
        e_mail = request.form["e_mail"]
        phone = request.form["phone"]
        description = request.form["description"]
        city = request.form["city"]
        address = request.form["address"]
        website = request.form["website"]

        if "logo" in request.files:
            logo = request.files["logo"]
            firm_db.update_firm_with_logo(firm_id, Firm(firm_name, password, e_mail, phone, city, address, website, description, logo.read()))
        else:
            firm_db.update_firm(firm_id,  Firm(firm_name, password, e_mail, phone, city, address, website, description,None))

        s = request.form["s"]

        uploaded_files = request.form.getlist("file[]")
        for i in range(int(s) + 1):
            temp = "image" + str(i)
            if temp in request.files:
                file = request.files[temp]
                firm_image_db.add_image(FirmImage(firm_id, file.read()))

        return redirect(url_for('firm_page', id = firm_id))

    else:
        return render_template("403_un_authorized.html")

def add_expedition():
    drivers = driver_db.get_drivers()
    vehicles = vehicle_db.get_vehicles()
    cities = {}
    terminals = terminalop.get_all_terminal()
    for t in terminals:
        if t[7] not in cities:
            cities[t[7]] = {'city_name': t[9], 'terminals': []}
        cities[t[7]]['terminals'].append({'id': t[0], 'name': t[1]})

    return render_template("firm/add_expedition.html", vehicles = vehicles, cities = cities, drivers= drivers)

def edit_expedition(expedition_id):
    expedition = expedition_db.get_expedition(expedition_id)
    expedition.expedition_id = expedition_id
    drivers = driver_db.get_drivers()
    vehicles = vehicle_db.get_vehicles()
    cities = {}
    terminals = terminalop.get_all_terminal()
    if expedition.document is not None:
        expedition.document_link = "/expedition/document/" + str(id)
    else:
        expedition.document_link = None
    for t in terminals:
        if t[7] not in cities:
            cities[t[7]] = {'city_name': t[9], 'terminals': []}
        cities[t[7]]['terminals'].append({'id': t[0], 'name': t[1]})

    return render_template("firm/edit_expedition.html", expedition = expedition, vehicles = vehicles, cities = cities, drivers= drivers)


def expedition_list():
    firm_id = session.get('firm_id')
    firm = firm_db.get_firm(firm_id)
    if firm_id is not None:
        firm.firm_id = firm_id
    expeditions = expedition_db.get_firms_expedition(firm_id)
    return render_template("firm/expedition_list.html", firm = firm , expeditions = expeditions)


def expedition_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    temp_expedition = expedition_db.get_expedition(id)
    if temp_expedition is None:
        return render_template("404_not_found.html")
    else:
        firm = firm_db.get_firm(temp_expedition.firm_id)
        firm.firm_id = id
        from_city = city_db.get_city(temp_expedition.from_ )
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.plane_category = vehicle_db.get_vehicle(temp_expedition.selected_plane).category
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name
        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(id)
        else:
            temp_expedition.document_link = None

        return render_template("firm/expedition.html", user = user, firm = firm, expedition = temp_expedition)


def buy_ticket(expedition_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    temp_expedition = expedition_db.get_expedition(expedition_id)
    if temp_expedition is None:
        return render_template("404_not_found.html")
    else:
        firm = firm_db.get_firm(temp_expedition.firm_id)
        firm.firm_id = id
        from_city = city_db.get_city(temp_expedition.from_ )
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name
        temp_expedition.expedition_id = expedition_id

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name

        seats = seat_db.get_seats_of_expedition(expedition_id)



        return render_template("ticket/buy.html", user = user, firm = firm, expedition = temp_expedition, seats = seats)


def edit_ticket(ticket_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    ticket = ticket_db.get_ticket(ticket_id)[0]
    temp_expedition = expedition_db.get_expedition(ticket.expedition_id)
    if temp_expedition is None:
        return render_template("404_not_found.html")
    else:
        firm = firm_db.get_firm(temp_expedition.firm_id)
        firm.firm_id = id
        from_city = city_db.get_city(temp_expedition.from_ )
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name
        temp_expedition.expedition_id = ticket.expedition_id

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name

        seats = seat_db.get_seats_of_expedition(ticket.expedition_id)
        ticket.ticket_id = ticket_id
        return render_template("ticket/edit.html", user = user, firm = firm, expedition = temp_expedition, seats = seats , ticket = ticket)


def my_tickets():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    tickets = ticket_db.get_tickets_of_users(user_id)
    for (id, ticket) in tickets:
        temp_expedition = expedition_db.get_expedition(ticket.expedition_id)
        firm = firm_db.get_firm(temp_expedition.firm_id)
        firm.firm_id = id
        from_city = city_db.get_city(temp_expedition.from_ )
        (city_code, city_name) = from_city
        temp_expedition.from_city = city_name
        to_city = city_db.get_city(temp_expedition.to)
        (city_code, city_name) = to_city
        temp_expedition.to_city = city_name
        if dayCompare(temp_expedition.date) and ticket.is_cancelable:
            ticket.is_cancelable = True
            ticket.editable = True
        elif dayCompare(temp_expedition.date):
            ticket.editable = True
        else:
            ticket.is_cancelable = False
            ticket.editable = False

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.plane_category = vehicle_db.get_vehicle(temp_expedition.selected_plane).category
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name
        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(id)

        else:
            temp_expedition.document_link = None


        ticket.expedition = temp_expedition
        ticket.firm = firm
        ticket.ticket_id = id

    return render_template("ticket/my_tickets.html", user = user, tickets = tickets)

def signup_page():
    error = ""
    try: 
        db_password = request.form['password']+salt
        h = hashlib.md5(db_password.encode())
        userid = userop.add_user(request.form['username'],request.form['name'],request.form['surname'],
                                request.form['gender'],request.form['mail'],h.hexdigest(),
                                request.form['phone'],request.form['address'])
        #print("userid: ",userid)
        #session['user_id'] = userid
        return redirect(url_for('login'))
    except IntegrityError:
        #print("duplicate entry")
        error = "duplicate entry"
        pass # TODO show error pop up for already existing user
    except:
        #print("generic errorrrrrrr",sys.exc_info())
        error = "error occured"
        pass # TODO show generic pop up error
    return render_template("signup.html",error = error)

def add_terminal_page(err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    cities = city_db.get_all_city()
    return render_template("terminal/add_terminal.html", cities = cities, user = user, err_msg =err_msg)

def terminals_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    terminals = terminalop.get_all_terminal_v2()
    return render_template("terminal/terminals.html", terminals = terminals, user = user)

def edit_terminal_page(id, err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    terminal = terminalop.get_terminal_wid(id)
    if terminal is None:
        return render_template("404_not_found.html")
    else:
        cities = city_db.get_all_city()
        return render_template("terminal/edit_terminal.html", terminal= terminal, cities = cities, user = user, err_msg=err_msg)

def add_sale_page(err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    firm = firm_db.get_firms()
    return render_template("sale/add_sale.html", firm = firm, user = user,err_msg=err_msg)

def sales_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    sales = sale_db.get_all_sales()
    return render_template("sale/sales.html", sales = sales, user = user)

def edit_sale_page(id, err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    sale = sale_db.get_sale(id)
    firms = firm_db.get_firms()

    if sale is None:
        return render_template("404_not_found.html")
    else:
        return render_template("sale/edit_sale.html", sale= sale, firms = firms, user = user,err_msg=err_msg)

def add_user_page(err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user is None:
        return render_template("404_not_found.html")
    else:
        return render_template("user/add_user.html", user=user,err_msg=err_msg)

def users_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    users = userop.get_all_user_listing()
    return render_template("user/users.html", users = users, user = user)

def edit_user_page(id,err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    edit_user = userop.get_user(id)
    if edit_user is None:
        return render_template("404_not_found.html")
    else:
        return render_template("user/edit_user.html", edit_user = edit_user, user = user,err_msg=err_msg)

def cities_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    cities = city_db.get_all_cities()
    return render_template("city/cities.html", cities = cities, user = user)

def add_city_page(err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    return render_template("city/add_city.html", user = user,err_msg=err_msg)

def edit_city_page(code,err_msg=""):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    str_code = ""
    if int(code) < 10 and int(code) > 0:
        str_code = "0"+str(code)
        city = city_db.get_city_all(str_code)
    else:
        city = city_db.get_city_all(str(code))
    
    if city is None:
        return render_template("404_not_found.html")
    else:
        return render_template("city/edit_city.html", city= city, user = user,err_msg=err_msg)



