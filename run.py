import os
import json
from flask import Flask, render_template, request, url_for, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app with template folder configuration
app = Flask(__name__, template_folder='taskmanager/templates')
app.secret_key = 'supersecretkey'

# Configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "supersecretkey")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL", "sqlite:///taskmanager.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Define constants
USERNAME = 'owner'
PASSWORD = 'pR_%6$?s'

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
    return render_template("base.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Define routes for the task manager
@app.route("/tasks")
def tasks():
    tasks = Task.query.all()
    categories = Category.query.all()
    return render_template("tasks.html", tasks=tasks, categories=categories)

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form.get("task_name")
        task_description = request.form.get("task_description")
        is_urgent = True if request.form.get("is_urgent") else False
        due_date = request.form.get("due_date")
        category_id = request.form.get("category_id")

        new_task = Task(task_name=task_name, task_description=task_description,
                        is_urgent=is_urgent, due_date=due_date, category_id=category_id)

        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("tasks"))

    categories = Category.query.all()
    return render_template("add_task.html", categories=categories)

@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = True if request.form.get("is_urgent") else False
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")

        db.session.commit()
        return redirect(url_for("tasks"))

    categories = Category.query.all()
    return render_template("update_task.html", task=task, categories=categories)

@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("tasks"))

# Initialize the database
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP", "0.0.0.0"), port=int(os.environ.get("PORT", "5000")), debug=os.environ.get("DEBUG", "True") == "True")
