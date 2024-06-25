# form_handler.py

import os
from flask import request, flash, redirect, url_for
from flask_mailman import Mail, EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Function to configure the Flask-Mailman extension
def configure_mail(app):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Using Gmail SMTP server
    app.config['MAIL_PORT'] = 587  # TLS port
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

    mail = Mail(app)
    return mail

# Function to handle form submission
def handle_form_submission(mail):
    name = request.form.get("first_name")
    phone = request.form.get("phone")
    email = request.form.get("email_address")
    message = request.form.get("textarea")
    performance_preference = request.form.get("performance_preference")

    # Send email
    msg = EmailMessage(
        subject="New Reservation Request",
        body=f"""
        Name: {name}
        Phone: {phone}
        Email: {email}
        Message: {message}
        Performance Preference: {performance_preference}
        """,
        to=[os.environ.get('MAIL_USERNAME')],
    )
    mail.send(msg)

    flash("Your reservation request has been sent.", "success")
