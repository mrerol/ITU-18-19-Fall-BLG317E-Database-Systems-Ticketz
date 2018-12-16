from flask import Flask, render_template, redirect, url_for, request, jsonify, session, send_file
from io import BytesIO
from urllib.parse import unquote


import views
from base64 import b64encode
from dao.user_dao import UserDao
from DBOP.tables.image_table import Image
from DBOP.tables.hotel_table import Hotel
from DBOP.tables.seat_table import Seat
from DBOP.tables.ticket_table import Ticket
from DBOP.tables.expedition_table import Expedition
from DBOP.hotel_db import hotel_database
from DBOP.image_db import image_database
from DBOP.expedition_db import expedition_database
from DBOP.vehicles_db import vehicle_database
from DBOP.seat_db import seat_database
from DBOP.ticket_db import ticket_database
from dao.terminal_dao import TerminalDao
from dao.sale_dao import SaleDao
from dao.city_dao import CityDao

terminalop = TerminalDao()


db_hotel = hotel_database()
db_image = image_database()
db_expedition = expedition_database()
db_vehicle = vehicle_database()
db_seat = seat_database()
db_ticket = ticket_database()

hotel_db = db_hotel.hotel
image_db = db_image.image
seat_db = db_seat.seat
ticket_db = db_ticket.ticket
expedition_db = db_expedition.expedition
vehicle_db = db_vehicle.vehicle
userop = UserDao()
sale_db = SaleDao()
city_db = CityDao()

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    return app

app = create_app()

app.secret_key = b'_5#y2L"F4Q8z_^?4c]/'


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404_not_found.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500_internal_error.html")

@app.route('/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.admin_home_page()
    else:
        return unAuth403()

@app.route('/hotels/', methods=['GET', 'POST'])
def hotels_page():
    return views.hotels_page()

@app.route('/search_hotel/<string:text>', methods=['GET', 'POST'])
def search_hotel(text):
    return views.search_hotel_page(text)

@app.route('/search_expedition/<string:text>', methods=['GET', 'POST'])
def search_expedition(text):
    text = text.replace("date", "/")
    return views.search_expedition_page(text)

@app.route('/search_ticket/<string:text>', methods=['GET', 'POST'])
def search_ticket(text):
    text = text.replace("date", "/")
    return views.search_ticket_page(text)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')
    firm_id = session.get('firm_id')
    if firm_id is None and user_id is None:
        user = userop.get_user(user_id)
        if user and user[-1]:
            return redirect(url_for('admin_home_page'))
        elif user and not user[-1]:
            return redirect(url_for('home_page'))
        else:
            return views.login_page(request)
    elif firm_id is not None:
        return redirect(url_for('firm_page', id=firm_id))
    elif user_id is not None:
        return redirect(url_for('home_page'))
    else:
        return render_template('500_internal_error.html')


@app.route('/admin/add_hotel', methods=['GET', 'POST'])
def add_hotel_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
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
            if "logo" in request.files:
                logo = request.files["logo"]
                hotel_db.add_hotel_with_logo(Hotel(hotel_name, email, description, city, address, phone, website, logo.read()))
            else:
                hotel_db.add_hotel(Hotel(hotel_name, email, description, city, address, phone, website, None))

            s = request.form["s"]

            (temp_id, ) = hotel_db.get_hotel_id(Hotel(hotel_name, email, description, city, address, phone, website, None))

            uploaded_files = request.form.getlist("file[]")
            for i in range(int(s) + 1):
                temp = "image" + str(i)
                if temp in request.files:
                    file = request.files[temp]
                    image_db.add_image(Image(temp_id, file.read()))

            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()

@app.route('/admin/edit_hotel/<int:id>', methods=['GET', 'POST'])
def edit_hotel_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    print(user)
    if user and user[-1]:
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
            if "logo" in request.files:
                logo = request.files["logo"]
                hotel_db.update_hotel_with_logo(id, Hotel(hotel_name, email, description, city, address, phone, website, logo.read()))
            else:
                hotel_db.update_hotel(id, Hotel(hotel_name, email, description, city, address, phone, website, None))
            s = request.form["s"]
            uploaded_files = request.form.getlist("file[]")
            for i in range(int(s) + 1):
                temp = "image" + str(i)
                if temp in request.files:
                    file = request.files[temp]
                    image_db.add_image(Image(id, file.read()))

            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()



@app.route('/admin/edit_hotels', methods=['GET', 'POST'])
def edit_hotels_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.edit_hotels_page()
    else:
        return unAuth403()

@app.route('/admin/edit_expeditions', methods=['GET', 'POST'])
def edit_expeditions_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.edit_expeditions_page()
    else:
        return unAuth403()

@app.route('/admin/delete_hotel/<int:id>')
def delete_hotel(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        hotel_db.delete_hotel(id)
        return redirect(url_for('edit_hotels_page'))
    else:
        return unAuth403()



@app.route('/admin/delete_image/<int:hotel_id>/<int:image_id>')
def delete_image(hotel_id, image_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        image_db.delete_image(hotel_id, image_id)
        return redirect(url_for('edit_hotel_page', id=hotel_id))
    else:
        return unAuth403()


@app.route('/admin/delete_logo/<int:hotel_id>')
def delete_hotel_logo(hotel_id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        hotel_db.delete_hotel_logo(hotel_id)
        return redirect(url_for('edit_hotel_page', id=hotel_id))
    else:
        return unAuth403()



@app.route('/hotels/<int:id>', methods=['GET', 'POST'])
def hotel_page(id):
    return views.hotel_page(id)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        return views.home_page()
    else:
        return views.filtered_home_page()

@app.route('/firm/<int:id>', methods=['GET', 'POST'])
def firm_page(id):
    return views.firm_page(id)

@app.route('/firm/edit_firmpage', methods=['GET', 'POST'])
def edit_firm_page():
    return views.edit_firm_page(request)


@app.route('/firm/login', methods=['GET', 'POST'])
def firm_login():
    user_id = session.get('user_id')
    print(user_id)
    firm_id = session.get('firm_id')
    if firm_id is None and user_id is None:
        return views.firm_login(request)
    elif firm_id is not None:
        return redirect(url_for('firm_page', id = firm_id))
    elif user_id is not None:
        return redirect(url_for('home_page'))
    else:
        return render_template('500_internal_error.html')


@app.route('/firm/logout', methods=['GET', 'POST'])
def firm_logout():
    return views.firm_logout()

@app.route('/firm/signup', methods=['GET', 'POST'])
def firm_signup():
    user_id = session.get('user_id')
    firm_id = session.get('firm_id')
    if firm_id is None and user_id is None:
        return views.firm_signup(request)
    elif firm_id is not None:
        return redirect(url_for('firm_page', id=firm_id))
    elif user_id is not None:
        return redirect(url_for('home_page'))
    else:
        return render_template('500_internal_error.html')



@app.route('/firm/add_driver', methods=['GET', 'POST'])
def add_driver():
    return views.add_driver_page(request)


@app.route('/firm/driver_list/<int:id>', methods=['GET', 'POST'])
def driver_list_page(id):
    firm_id = session.get('firm_id')
    if firm_id == id:
        return views.driver_list_page(id)
    else:
        return unAuth403()

@app.route('/search_driver/<string:search_for>', methods=['GET', 'POST'])
def search_driver_page(search_for):
    return views.search_driver_page(search_for)

@app.route('/firm/driver_edit/<int:driver_id>', methods=['GET', 'POST'])
def driver_edit_page(driver_id):
    return views.driver_edit_page(request, driver_id)

@app.route('/firm/delete_driver/<int:driver_id>', methods=['GET', 'POST'])
def driver_delete_page(driver_id):
    return views.driver_delete_page(driver_id)

@app.route('/firm/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    return views.add_vehicle_page(request)

@app.route('/firm/vehicle_list/<int:id>', methods=['GET', 'POST'])
def vehicle_list_page(id):
    firm_id = session.get('firm_id')
    if firm_id == id:
        return views.vehicle_list_page(id)
    else:
        return unAuth403()

@app.route('/search_vehicle/<string:search_for>', methods=['GET', 'POST'])
def search_vehicle_page(search_for):
    return views.search_vehicle_page(search_for)

@app.route('/firm/vehicle_edit/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_edit_page(vehicle_id):
    return views.vehicle_edit_page(request,vehicle_id)

@app.route('/firm/delete_vehicle/<int:vehicle_id>', methods=['GET', 'POST'])
def vehicle_delete_page(vehicle_id):
    return views.vehicle_delete_page(vehicle_id)

@app.route('/firm/add_expedition', methods=['GET', 'POST'])
def add_expedition():
    firm_id = session.get("firm_id")
    if firm_id != None:
        if request.method == "GET":
            return views.add_expedition()
        else:
            from_ = request.form["from"]
            from_ter = request.form["from_ter"]
            to = request.form["to"]
            to_ter = request.form["to_ter"]
            dep_time = request.form["dep_time"]
            arr_time = request.form["arr_time"]
            date = request.form["date"]
            price = request.form["price"]
            plane = request.form["selected_plane"]
            vehicle = vehicle_db.get_vehicle(plane)
            total_cap = vehicle.capacity
            driver_id  = request.form["driver"]
            if "document" in request.files:
                document = request.files["document"]
                expedition_db.add_expedition_with_document(Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0, document.read()))

            else:
                expedition_db.add_expedition(Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0,  None ))

            return redirect(url_for('firm_page', id=firm_id))
    else:
        return unAuth403()


@app.route('/firm/edit_expedition/<int:expedition_id>', methods=['GET', 'POST'])
def edit_expedition(expedition_id):
    firm_id = session.get("firm_id")
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    temp_firm_id = expedition_db.get_expedition(expedition_id).firm_id
    if (firm_id != None and firm_id is temp_firm_id ) or user[-1]:
        if request.method == "GET":
            return views.edit_expedition(expedition_id)
        else:
            from_ = request.form["from"]
            from_ter = request.form["from_ter"]
            to = request.form["to"]
            to_ter = request.form["to_ter"]
            dep_time = request.form["dep_time"]
            arr_time = request.form["arr_time"]
            date = request.form["date"]
            price = request.form["price"]
            plane = request.form["selected_plane"]
            vehicle = vehicle_db.get_vehicle(plane)
            total_cap = vehicle.capacity
            driver_id  = request.form["driver"]
            if "document" in request.files:
                document = request.files["document"]
                expedition_db.update_expedition_with_document(expedition_id ,Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0, document.read()))

            else:
                expedition_db.update_expedition(expedition_id, Expedition(from_, from_ter, to, to_ter, dep_time, arr_time, date, price, plane, driver_id, firm_id, total_cap, 0,  None ))

            return redirect(url_for('firm_page', id=firm_id))
    else:
        return unAuth403()



@app.route('/firm/expedition_list', methods=['GET', 'POST'])
def expedition_list():
    firm_id = session.get('firm_id')
    if firm_id:
        return views.expedition_list()
    else:
        return unAuth403()

@app.route('/firm/expedition/<int:id>', methods=['GET', 'POST'])
def expedition_page(id):
    return views.expedition_page(id)

@app.route('/expedition/document/<int:expedition_id>', methods=['GET'])
def expedition_document(expedition_id):
    file_data = expedition_db.get_expedition(expedition_id).document
    file_name = str(expedition_id) + '.pdf'
    return send_file(BytesIO(file_data), attachment_filename = file_name, as_attachment=True)


@app.route('/expedition/document/delete_document/<int:expedition_id>')
def delete_expedition_document(expedition_id):
    firm_id = session.get('firm_id')
    if firm_id == expedition_db.get_expedition(expedition_id).firm_id:
        expedition_db.delete_expedition_document(expedition_id)
        return "<script>alert('document has been deleted sucsessfuly'); window.close();</script>"
    else:
        return unAuth403()

@app.route('/firm/delete_expedition/<int:expedition_id>')
def delete_expedition(expedition_id):
    firm_id = session.get('firm_id')
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if firm_id == expedition_db.get_expedition(expedition_id).firm_id or user[-1]:
        expedition_db.delete_expedition(expedition_id)
        if user[-1]:
            return redirect(url_for('edit_expeditions_page'))
        else:
            return redirect(url_for('expedition_list'))
    else:
        return unAuth403()


@app.route('/ticket/buy/<int:expedition_id>', methods=["POST", "GET"])
def buy_ticket(expedition_id):

    user_id = session.get('user_id')
    if user_id != None:
        if request.method == "POST":
            temp_expedition = expedition_db.get_expedition(expedition_id)
            if temp_expedition.current_cap < temp_expedition.total_cap:
                if request.form.getlist('seat'):
                    seat_number = request.form["seat"]
                    is_cancellable = request.form["is_cancelable"]
                    extra_baggage = request.form["extra_baggage"]
                    seat_db.add_seat(Seat(expedition_id, user_id, seat_number))
                    temp_expedition = expedition_db.get_expedition(expedition_id)
                    sale = sale_db.get_sale_price(temp_expedition.firm_id, user_id)
                    price = temp_expedition.price
                    if sale is not None:
                        price -= sale[0]
                    ticket_db.add_ticket(Ticket(expedition_id, user_id, seat_number, temp_expedition.firm_id, price, extra_baggage, is_cancellable))
                    expedition_db.bought(expedition_id)

                    hotel_city = city_db.get_city(temp_expedition.to)
                    (city_code, city_name) = hotel_city
                    print(city_name)


                    return redirect(url_for('search_hotel', text = city_name))
                else:
                    return views.buy_ticket(expedition_id)
            else:
                return redirect(url_for('/'))
        else:
            return views.buy_ticket(expedition_id)
    else:
        return unAuth403()

@app.route('/ticket/edit/<int:ticket_id>', methods=["POST", "GET"])
def edit_ticket(ticket_id):

    user_id = session.get('user_id')
    if user_id != None:
        if request.method == "POST":
            ticket = ticket_db.get_ticket(ticket_id)
            if len(ticket) is not 0:
                ticket = ticket_db.get_ticket(ticket_id)[0]
                temp_expedition = expedition_db.get_expedition(ticket.expedition_id)
                if temp_expedition.current_cap < temp_expedition.total_cap:
                    if request.form.getlist('seat'):
                        seat_number = request.form["seat"]
                        is_cancellable = request.form["is_cancelable"]
                        extra_baggage = request.form["extra_baggage"]
                        print(is_cancellable, extra_baggage)
                        seat_db.update_seat_number(Seat(ticket.expedition_id, ticket.user_id, ticket.seat_number), seat_number)
                        ticket_db.update_ticket(Ticket(ticket.expedition_id, ticket.user_id, ticket.seat_number, ticket.firm_id, ticket.price, ticket.extra_baggage, ticket.is_cancelable), seat_number, is_cancellable, extra_baggage)
                        return redirect(url_for('my_tickets'))
                    else:
                        return views.edit_ticket(ticket_id)
                else:
                    return redirect(url_for('/'))
            else:
                render_template('404_not_found.html')
        else:
            ticket = ticket_db.get_ticket(ticket_id)
            if len(ticket) is not 0:
                return views.edit_ticket(ticket_id)
            else:
                return render_template('404_not_found.html')
    else:
        return unAuth403()


@app.route('/ticket/delete/<int:ticket_id>')
def delete_ticket(ticket_id):
    user_id = session.get('user_id')
    ticket = ticket_db.get_ticket(ticket_id)
    if ticket is not None:
        if user_id[0] == ticket[0].user_id:
            ticket_db.delete_ticket(ticket_id)
            expedition_db.cancelled(ticket[0].expedition_id)
            seat_db.delete_seat(Seat(ticket[0].expedition_id, ticket[0].user_id, ticket[0].seat_number))
            return "<script>alert('ticket has been deleted sucsessfuly'); window.close();</script>"
        else:
            return unAuth403()
    else:
        return unAuth403()


@app.route('/my_tickets', methods=['GET', 'POST'])
def my_tickets():
    user_id = session.get('user_id')
    if user_id:
        return views.my_tickets()
    else:
        return unAuth403()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_id = session.get('user_id')
    firm_id = session.get('firm_id')
    if firm_id is None and user_id is None:
        return views.signup_page()
    elif firm_id is not None:
        return redirect(url_for('firm_page', id=firm_id))
    elif user_id is not None:
        return redirect(url_for('home_page'))
    else:
        return render_template('500_internal_error.html')



@app.route('/403')
def unAuth403():
    return render_template('403_un_authorized.html')



## for AJAX
@app.route('/get_city_of_terminal_with_city_id/<string:city_id>', methods=['POST'])
def get_city_of_terminal_with_city_id(city_id):
    terminals = terminalop.get_all_terminal_city_wcity_id(city_id)
    print(terminals)
    return jsonify(terminals)

@app.route('/admin/add_terminal', methods=['GET', 'POST'])
def add_terminal_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET": 
            return views.add_terminal_page()
        else:
            terminalop.add_terminal(request.form['terminal_name'],request.form['terminal_code'],request.form['e_mail'],
                                        request.form['phone'],request.form['address'],request.form['description'],
                                        request.form['city'])
            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()

@app.route('/admin/terminals', methods=['GET', 'POST'])
def terminals_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.terminals_page()
    else:
        return unAuth403()


@app.route('/admin/delete_terminal/<int:id>',  methods=['GET', 'POST'])
def delete_terminal(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        terminalop.delete_terminal(id)
        return redirect(url_for('terminals_page'))
    else:
        return unAuth403()

@app.route('/admin/edit_terminal/<int:id>', methods=['GET', 'POST'])
def edit_terminal_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET":
            print("*****************test1***")
            return views.edit_terminal_page(id)
        else:
            print("*****************test2***")
            terminalop.edit_terminal(id,request.form['terminal_name'],request.form['terminal_code'],request.form['e_mail'],request.form['phone'],request.form['address'],request.form['description'],request.form['city'] )
            return redirect(url_for('edit_terminal_page', id=id))
    else:
        return unAuth403()


@app.route('/admin/add_sale', methods=['GET', 'POST'])
def add_sale_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET": 
            return views.add_sale_page()
        else:
            sale_db.add_sale(request.form['sale_code'],request.form['sale_start_at'],request.form['sale_finish_at'],
                                        request.form['description'],request.form['is_active'],request.form['firm'],
                                        request.form['sale_price'])
            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()

@app.route('/admin/sales', methods=['GET', 'POST'])
def sales_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.sales_page()
    else:
        return unAuth403()

@app.route('/admin/delete_sale/<int:id>',  methods=['GET', 'POST'])
def delete_sale(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        sale_db.delete_sale(id)
        return redirect(url_for('sales_page'))
    else:
        return unAuth403()


@app.route('/admin/edit_sale/<int:id>', methods=['GET', 'POST'])
def edit_sale_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET":
            return views.edit_sale_page(id)
        else:
            sale_db.edit_sale(id,request.form['sale_code'],request.form['sale_start_at'],request.form['sale_finish_at'],request.form['description'],request.form['is_active'],request.form['firm'],request.form['sale_price'] )
            return redirect(url_for('edit_sale_page', id=id))
    else:
        return unAuth403()


@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET": 
            return views.add_user_page()
        else:
            userop.add_user_with_adminfo(request.form['user_name'],request.form['name'],request.form['surname'],
                                        request.form['gender'],request.form['email'],request.form['password'],
                                        request.form['phone'],request.form['address'],request.form['is_admin'])
            return redirect(url_for('admin_home_page'))
    else:
        return unAuth403()

@app.route('/admin/users', methods=['GET', 'POST'])
def users_page():
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        return views.users_page()
    else:
        return unAuth403()

@app.route('/admin/delete_user/<int:id>',  methods=['GET', 'POST'])
def delete_user(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        userop.delete_user(id)
        return redirect(url_for('users_page'))
    else:
        return unAuth403()

@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user_page(id):
    user_id = session.get('user_id')
    user = userop.get_user(user_id)
    if user and user[-1]:
        if request.method == "GET":
            return views.edit_user_page(id)
        else:
            #user_id,user_name, name, surname, gender, email, password, phone, address, is_admin
            userop.edit_user(id,request.form['user_name'],request.form['name'],request.form['surname'],
                                        request.form['gender'],request.form['email'],request.form['password'],
                                        request.form['phone'],request.form['address'],request.form['is_admin'])
            return redirect(url_for('edit_user_page', id=id))
    else:
        return unAuth403()

if __name__ == "__main__":
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
