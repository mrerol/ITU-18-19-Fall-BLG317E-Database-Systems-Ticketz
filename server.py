from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home_page():
    return "Hello, world!"

@app.route("/admin_home_page")
def admin_home_page():
    return render_template("admin_home_page.html")

if __name__ == "__main__":
    app.run()
