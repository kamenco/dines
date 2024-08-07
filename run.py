import os
import json
from flask import Flask, render_template, request, url_for, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form_handler import configure_mail, handle_form_submission
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app with template folder configuration
app = Flask(__name__, static_folder='taskmanager/static', template_folder='taskmanager/templates')
app.secret_key = 'supersecretkey'

# Configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL", "sqlite:///taskmanager.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Configure the mail
mail = configure_mail(app)

# Define constants
USERNAME = 'owner'
PASSWORD = 'pR_%6$?s'

# Load recipes from JSON file
def load_recipes():
    with open('taskmanager/static/data/list.json') as f:
        return json.load(f)

# Define database models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)

    def __repr__(self):
        return self.category_name


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "#{0} - Task: {1} | Urgent: {2}".format(self.id, self.task_name, self.is_urgent)

# Define routes for the existing site
@app.route("/")
def home():
    return render_template("index.html", page_title="Welcome to Varna Eats")

@app.route("/menu")
def menu():
    recipes = load_recipes()
    # Filter recipes based on category if a category is selected
    category = request.args.get('category', '')
    if category:
        recipes = [recipe for recipe in recipes if recipe['category'] == category]

    page_title = "Menu"
    return render_template("menu.html", list=recipes, page_title=page_title)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        handle_form_submission(mail)
        return redirect(url_for("contact"))

    return render_template("contact.html")

# Define routes for login logout
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            flash("You are now logged in.", "success")
            return redirect(url_for("update_menu"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("login.html", page_title="Login")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You are now logged out.", "success")
    return redirect(url_for("home"))

# Define route for update_menu
@app.route('/update_menu', methods=['GET', 'POST'])
def update_menu():
    recipes = load_recipes()

    if request.method == 'POST':
        if 'add' in request.form:
            new_recipe = {
                "name": request.form['name'],
                "description": request.form['description'],
                "image": request.form['image'],
                "category": request.form['category']
            }
            recipes.append(new_recipe)
            with open('taskmanager/static/data/list.json', 'w') as f:
                json.dump(recipes, f, indent=4)
            flash('Successfully added the recipe!', 'success')
        
        elif 'delete' in request.form:
            recipe_name = request.form['recipe_name']
            recipes = [recipe for recipe in recipes if recipe['name'] != recipe_name]
            with open('taskmanager/static/data/list.json', 'w') as f:
                json.dump(recipes, f, indent=4)
            flash('Successfully deleted the recipe!', 'success')
        
        return redirect(url_for('update_menu'))

    return render_template('update_menu.html', page_title="Update Menu", list=recipes)



# Define routes for the task manager

@app.route("/tasks")
def tasks():
    try:
        tasks = Task.query.all()
        categories = Category.query.all()

        return render_template("tasks.html", tasks=tasks, categories=categories)
    except Exception as e:
        # Log the exception and flash an error message
        print(f"Error: {e}")
        flash("An error occurred while loading tasks.", "danger")
        return redirect(url_for("home"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    try:
        if request.method == "POST":
            task_name = request.form.get("task_name")
            task_description = request.form.get("task_description")
            is_urgent = True if request.form.get("is_urgent") else False
            due_date_str = request.form.get("due_date")
            category_id = request.form.get("category_id")

            # Check if a task with the same name already exists
            existing_task = Task.query.filter_by(task_name=task_name).first()
            if existing_task:
                flash("A task with that name already exists. Please choose a different name.", "danger")
                return redirect(url_for("add_task"))

            # Convert due_date from string to date object
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError as ve:
                flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
                return redirect(url_for("add_task"))

            new_task = Task(task_name=task_name, task_description=task_description,
                            is_urgent=is_urgent, due_date=due_date, category_id=category_id)

            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully.", "success")
            return redirect(url_for("tasks"))

        categories = Category.query.all()
        return render_template("add_task.html", categories=categories)
    except Exception as e:
        flash("An error occurred while adding the task.", "danger")
        return redirect(url_for("tasks"))


@app.route("/test_db")
def test_db():
    try:
        task = Task.query.first()
        if task:
            return f"Task exists: {task.task_name}"
        else:
            return "No tasks found."
    except Exception as e:
        return f"Database error: {e}"


@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = True if request.form.get("is_urgent") else False
        due_date_str = request.form.get("due_date")

        # Convert due_date from string to date object
        try:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
            return redirect(url_for("update_task", task_id=task_id))

        task.category_id = request.form.get("category_id")

        db.session.commit()
        return redirect(url_for("tasks"))

    categories = Category.query.all()
    return render_template("update_task.html", task=task, categories=categories)


@app.route("/delete_task/<int:task_id>", methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully.", "success")
    return redirect(url_for("tasks"))



# Initialize the database and add initial categories if none exist
with app.app_context():
    db.create_all()  # Ensure all tables are created
    # Check if any categories exist
    if not Category.query.first():
        # Add initial categories
        initial_categories = ["Work", "Personal", "Hobby"]
        for category_name in initial_categories:
            db.session.add(Category(category_name=category_name))
        db.session.commit()


if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)

