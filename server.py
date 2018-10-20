from flask import Flask, render_template
import views

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/admin_home_page", view_func=views.admin_home_page)
    app.add_url_rule("/hotels/<int:id>", view_func=views.hotel_page)
    return app



if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="127.0.0.1", port=port)
