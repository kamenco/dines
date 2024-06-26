# Varna Eats


[Click on this link to visit the site on Heroku](https://dines-kamen-9b44aac7c04a.herokuapp.com/)

Varna Eats is a web application that allows users to view the menu, make reservations, and manage tasks. This project is built using Flask and is deployed on Heroku.

## Features

- View the menu with various recepies.
- Make reservations through a contact form.
- Login and manage the menu (add or delete recipes).
- Task management functionality including adding, updating, and deleting tasks.

## Project Structure

|-- run.py
|-- form_handler.py
|-- env.py
|-- requirements.txt
|-- taskmanager/ 
| |-- init.py
| |-- templates/
| | |-- base.html
| | |-- index.html
| | |-- menu.html
| | |-- contact.html
| | |-- login.html
| | |-- update_menu.html
| | |-- tasks.html
| | |-- add_task.html
| | |-- update_task.html
|-- .env


Clone the repository


## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/varna-eats.git
   cd varna-eats
Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
 Install dependancies

 pip install -r requirements.txt

Set up environment variables, create an env.py file
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///taskmanager.db
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password


Initialize the database

flask db init
flask db migrate -m "Initial migration."
flask db upgrade



# Bug fixes

Check if task with the same name already exists. If it exists the program crashes. 


![The integrity error!](taskmanager/static/images/unique_name_error.png "The integrity error")



The bug was solved with adding the code check if a task with the same name already exists
        
        
        existing_task = Task.query.filter_by(task_name=task_name).first()
        if existing_task:
            flash("A task with that name already exists. Please choose a different name.", "danger")
            return redirect(url_for("add_task"))