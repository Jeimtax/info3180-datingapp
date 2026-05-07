from app import app, db
from .models import User, Profile
from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from .forms import RegistrationForm, ProfileForm

api = Blueprint('api', __name__)

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@api.route('/register', methods=['POST'])
def register():
    reg_form = RegistrationForm()
    prof_form = ProfileForm()

    if reg_form.validate_on_submit() and prof_form.validate_on_submit():
        
        if User.query.filter_by(email=reg_form.email.data).first():
            return jsonify({"errors": ["Email already registered"]}), 400
        
        file = prof_form.profile_pic.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            user = User(
                username=reg_form.username.data,
                email=reg_form.email.data,
                password_hash=generate_password_hash(reg_form.password.data)
            )
            db.session.add(user)
            db.session.flush()

            profile = Profile(
                user_id=user.id,
                first_name=prof_form.first_name.data,
                last_name=prof_form.last_name.data,
                age=prof_form.age.data,
                gender=prof_form.gender.data,
                location=prof_form.location.data,
                bio=prof_form.bio.data,
                hobbie1=prof_form.hobbie1.data,
                hobbie2=prof_form.hobbie2.data,
                hobbie3=prof_form.hobbie3.data,
                relationship_goal=prof_form.relationship_goal.data,
                profile_pic=filename,
                visibility=prof_form.visibility.data
            )
            db.session.add(profile)
            db.session.commit()

            return jsonify({
                "message": "User and Profile successfully created",
                "user_id": user.id
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [f"Database error: {str(e)}"]}), 500
    
    errors = form_errors(reg_form) + form_errors(prof_form)
    return jsonify({"errors": errors}), 400
    
    
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