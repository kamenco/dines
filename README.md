# Varna Eats

Varna Eats is a web application that allows users to view the menu, make reservations, and manage tasks. This project is built using Flask and is deployed on Heroku.

## Features

- View the menu with various recipes.
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
