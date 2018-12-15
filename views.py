from flask import render_template, redirect, url_for, request, session
from dao.user_dao import UserDao
from psycopg2 import IntegrityError
import sys
from base64 import b64encode

from DBOP.tables.firms_table import Firm
from DBOP.tables.drivers_table import Driver
from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database
from DBOP.seat_db import seat_database
from DBOP.ticket_db import ticket_database
from DBOP.firms_db import firm_database
from DBOP.vehicles_db import vehicle_database
from DBOP.drivers_db import driver_database
from DBOP.expedition_db import expedition_database
from dao.city_dao import CityDao
from dao.terminal_dao import TerminalDao

from DBOP.tables.expedition_table import Expedition
from DBOP.tables.ticket_table import Ticket


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
vehicle_db = db_vehicle.vehicle
driver_db = db_driver.driver
expedition_db = db_expedition.expedition
seat_db = db_seat.seat
ticket_db = db_ticket.ticket

userop = UserDao()
city_db = CityDao()
terminalop = TerminalDao()

def home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    firms = firm_db.get_firms()
    expeditions = expedition_db.get_all_expeditions()
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

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.plane_category = vehicle_db.get_vehicle(temp_expedition.selected_plane).category
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name
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

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.plane_category = vehicle_db.get_vehicle(temp_expedition.selected_plane).category
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name
        if temp_expedition.document is not None:
            temp_expedition.document_link = "/expedition/document/" + str(expedition_id)
        else:
            temp_expedition.document_link = None


    return render_template("home_page.html", user=user, expeditions = expeditions, cities = cities, firms = firms)




def admin_home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)

    return render_template("admin/admin_home_page.html", user = user)


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
    hotels = hotel_db.search(text)
    for (id , hotel) in hotels:
        if hotel.logo is not None:
            temp = b64encode(hotel.logo).decode("utf-8")
            hotel.logo = temp
    return render_template("hotel/hotel_list.html", hotels = (hotels), user = user)

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

        from_ter = terminalop.get_terminal_wid(temp_expedition.from_ter)
        temp_expedition.from_ter_name = from_ter[1]
        to_ter = terminalop.get_terminal_wid(temp_expedition.to_ter)
        temp_expedition.to_ter_name = to_ter[1]

        temp_expedition.plane_name = vehicle_db.get_vehicle(temp_expedition.selected_plane).name
        temp_expedition.plane_category = vehicle_db.get_vehicle(temp_expedition.selected_plane).category
        temp_expedition.driver_name = driver_db.get_driver(temp_expedition.driver_id).name
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
    error = None
    if request.method == 'POST':
        try:
            user_id = userop.get_user_id(request.form['username'],request.form['password'])
            print("userid ",user_id)
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


def add_driver_page(request):
    #session.permanent = True
    firm_id = session.get('firm_id')

    if firm_id is None:
        return render_template("un_authorized.html")

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

        if "logo" in request.files:
            logo = request.files["logo"]
            driver_db.add_driver_with_logo(
                Driver(driver_name, e_mail, gender, city, address, phone, '0', '0', logo.read()))
        else:
            driver_db.add_driver(Driver(driver_name, e_mail, gender, city, address, phone, '0', '0', None))

        return redirect(url_for('driver_list_page', id=firm_id))

    else:
        return render_template("un_authorized.html")

def driver_list_page(id):
    #session.permanent = True
    drivers = driver_db.get_drivers();
    return render_template("driver/driver_list.html",drivers=drivers)

def driver_profile_page(id):
    return render_template("driver/driver_profile.html")

def driver_edit_page(firm_id,driver_id):

    temp_id = session.get('firm_id')
    if temp_id != firm_id or temp_id is None:
        return render_template("un_authorized.html")

    driver=driver_db.get_driver(driver_id)

    if driver is None:
        return render_template("un_authorized.html")

    temp=driver_db.get_firm_ids(driver_id)

    for item in temp:
        (temp_item,)=item
        #print(temp_item)
        #print(driver_id)
        if temp_item != driver_id:
            return render_template("un_authorized.html")

    city=city_db.get_city(driver.city)
    (thresh,temp_city)=city
    return render_template("driver/driver_edit.html",driver=driver, city=temp_city)

def driver_delete_page(firm_id,driver_id):
    return ("sds")

def add_vehicle_page(request):
    #session.permanent = True
    firm_id = session.get('firm_id')

    if firm_id == None:
        return render_template("un_authorized.html")

    if request.method == "GET":
        return render_template("vehicle/add_vehicle.html")
    elif request.method == "POST":
         print("sa")
    else:
        return render_template("un_authorized.html")

def vehicle_list_page(id):
    #session.permanent = True
    drivers = driver_db.get_drivers();
    return render_template("vehicle/vehicle_list.html",drivers=drivers)

def firm_page(id):
    firm_id = session.get('firm_id')
    if id != firm_id:
        return render_template("un_authorized.html")
    elif id == firm_id:
        firm = firm_db.get_firm(firm_id)
        if firm is None:
            return render_template("404_not_found.html")
        else:
            toSend = []
            #images = image_db.get_images()
            if firm.logo is not None:
                firm.logo = b64encode(firm.logo).decode("utf-8")
            """for ( temp_id, trash, image) in images:
                if temp_id is id:
                    toSend.append(b64encode(image.file_data).decode("utf-8"))"""

            city = city_db.get_city(firm.city)
            #print(city)
            (code, city_name) = city
            return render_template("firm/firm.html", firm=firm, city_name = city_name, firm_id=id)
    else:
        return render_template("un_authorized.html")

def firm_signup(request):
    error = None
    if request.method == "GET":
        cities = city_db.get_all_city()
        return render_template("firm/signup.html", error=error, cities=cities)
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
            firm_db.add_firm_with_logo(
                Firm(firm_name, password, e_mail, phone, city, address, website, description, logo.read()))
        else:
            firm_db.add_firm(Firm(firm_name, password, e_mail, phone, city, address, website, description, None))

        s = request.form["s"]

        (temp_id,) = firm_db.get_firm_id(
            Firm(firm_name, password, e_mail, phone, city, address, website, description, None))
        """"
        uploaded_files = request.form.getlist("file[]")
        for i in range(int(s) + 1):
            temp = "image" + str(i)
            if temp in request.files:
                file = request.files[temp]
                image_db.add_image(Image(temp_id, file.read()))
        """
        return redirect(url_for('firm_login'))
    else:
        return render_template("un_authorized.html")


def firm_login(request):
    if request.method == "POST":
        email = request.form['e_mail']
        password = request.form['password']
        try:
            temp = firm_db.get_firm_id_login(email, password)
            (firm_id,) = temp
            #print(firm_id)
            if firm_id is not None:
                session.permanent = True
                session['firm_id'] = firm_id
                return redirect(url_for('firm_page', id=firm_id))
            else:
                return render_template("un_authorized.html")
        except:
            print("exception", sys.exc_info())

        return render_template("un_authorized.html")

    elif request.method == "GET":
        return render_template("firm/login.html")
    else:
        return render_template("404_not_found.html")

def firm_logout():
    session.permanent=False
    session['firm_id'] = False
    return redirect(url_for('firm_login'))

def add_expedition():
    drivers = driver_db.get_drivers()
    vehicles = vehicle_db.get_vehicles()
    cities = {}
    terminals = terminalop.get_all_terminal()
    for t in terminals:
        if t[7] not in cities:
            cities[t[7]] = {'city_name': t[-1], 'terminals': []}
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
            cities[t[7]] = {'city_name': t[-1], 'terminals': []}
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

