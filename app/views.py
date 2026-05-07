from app import app
from .models import *
from flask import Blueprint, render_template, request, jsonify, send_file, session
import os
from werkzeug.security import generate_password_hash

api = Blueprint('api', __name__)
###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

api.route('auth/register', methods=["POST"])
def register():
    data = request.get_json()


    if User.query.filter_by(email=data["email"]).first():
        return jsonify("Error: Email already registered"), 400
    
    user = User(
        email = data["email"].lower().strip(),
        username = data["username"].strip(),
        password_hash = generate_password_hash(data["password"])
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created", "user_id": user.id}), 201








###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404