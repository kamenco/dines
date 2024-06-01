import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERNAME = 'owner'
PASSWORD = 'password'

@app.route("/")
def index():
    return render_template("index.html", page_title="Home")

@app.route("/menu")
def menu():
    data = []
    with open("data/list.json", "r") as json_data:
        data = json.load(json_data)
    
    category = request.args.get('category')
    if category:
        data = [item for item in data if item['category'] == category]
    
    return render_template("menu.html", page_title="Menu", list=data)

@app.route("/contact")
def contact():
    return render_template("contact.html", page_title="Contact")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            flash('You were logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid Credentials', 'danger')
    return render_template("login.html", page_title="Login")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('index'))

@app.route("/update_menu", methods=['GET', 'POST'])
def update_menu():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    data = []
    with open("data/list.json", "r") as json_data:
        data = json.load(json_data)
    
    if request.method == 'POST':
        if 'add' in request.form:
            new_recipe = {
                "name": request.form['name'],
                "description": request.form['description'],
                "image": request.form['image'],
                "category": request.form['category']
            }
            data.append(new_recipe)
            with open("data/list.json", "w") as json_data:
                json.dump(data, json_data, indent=4)
            flash('Recipe added', 'success')
        elif 'delete' in request.form:
            recipe_name = request.form['recipe_name']
            data = [item for item in data if item['name'] != recipe_name]
            with open("data/list.json", "w") as json_data:
                json.dump(data, json_data, indent=4)
            flash('Recipe deleted', 'success')
        return redirect(url_for('update_menu'))
    
    return render_template("update_menu.html", page_title="Update Menu", list=data)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True
    )
