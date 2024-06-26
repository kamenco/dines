from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Define route for update_menu

@app.route("/update_menu", methods=["GET", "POST"])
def update_menu():
    if not session.get('logged_in'):
        flash("You need to be logged in to access this page.", "danger")
        return redirect(url_for('login'))

    # Handle form submissions for adding or deleting recipes
    if request.method == "POST":
        if 'add' in request.form:
            # Add new recipe logic here
            pass
        elif 'delete' in request.form:
            # Delete recipe logic here
            pass

    with open('taskmanager/static/data/list.json') as f:
        recipes = json.load(f)
    
    return render_template("update_menu.html", list=recipes, page_title="Update Menu")


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
