import os
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", page_title="Home")

@app.route("/menu")
def menu():
    data = []
    with open ("data/list.json", "r") as json_data:
        data =json.load(json_data)
    return render_template("menu.html", page_title="Menu", list=data)

@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact")

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )
