from app import app, db
from .models import User, Profile, Match
from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm, ProfileForm
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@api.route('/register', methods=['POST'])
def register():
    if request.is_json:
        data = request.get_json()
        try:
            user = User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )
            db.session.add(user)
            db.session.flush()

            profile = Profile(
                user_id=user.id,
                first_name=data.get('first_name', 'New'),
                last_name=data.get('last_name', 'User'),
                location=data.get('location', 'Unknown'),
                bio=data.get('bio', ''),
                visibility='public'
            )
            db.session.add(profile)
            db.session.commit()
            return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 500

    reg_form = RegistrationForm()
    prof_form = ProfileForm()

    if reg_form.validate_on_submit() and prof_form.validate_on_submit():
        if User.query.filter_by(email=reg_form.email.data).first():
            return jsonify({"errors": ["Email already registered"]}), 400
        
        filename = "default.png"
        if prof_form.profile_pic.data:
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

   
@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify(message="Login successful", token=access_token), 200
    
    return jsonify(error="Invalid username or password"), 401


@api.route('/explore', methods=['GET'])
@jwt_required()
def explore():
    current_user_id = get_jwt_identity()
    liked_ids = [m.target_id for m in Match.query.filter_by(user_id=current_user_id).all()]
    liked_ids.append(current_user_id)
    
    profiles = Profile.query.filter(~Profile.user_id.in_(liked_ids)).all()
    return jsonify(profiles=[{
        "id": p.user_id, 
        "name": f"{p.first_name} {p.last_name}",
        "bio": p.bio,
        "pic": p.profile_pic
    } for p in profiles])


@api.route('/like', methods=['POST'])
@jwt_required()
def like_user():
    current_user_id = get_jwt_identity()
    target_id = request.json.get('target_id')
    
    new_match = Match(user_id=current_user_id, target_id=target_id, status='like')
    db.session.add(new_match)
    
    # Check for mutual match
    mutual = Match.query.filter_by(user_id=target_id, target_id=current_user_id).first()
    db.session.commit()
    
    return jsonify(is_match=bool(mutual))


@api.route('/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    profile = Profile.query.filter_by(user_id=current_user_id).first()
    
    if not user or not profile:
        return jsonify(error="Profile not found"), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "location": profile.location,
        "bio": profile.bio,
        "pic": profile.profile_pic or 'default.png'
    }), 200


@api.route('/matches', methods=['GET'])
@jwt_required()
def get_matches():
    current_user_id = get_jwt_identity()
    
    matched_relations = Match.query.filter_by(user_id=current_user_id, status='like').all()
    
    matches_data = []
    for m in matched_relations:
        # Check if the other person liked us back
        mutual = Match.query.filter_by(user_id=m.target_id, target_id=current_user_id, status='like').first()
        
        if mutual:
            other_user = Profile.query.filter_by(user_id=m.target_id).first()
            if other_user:
                matches_data.append({
                    "id": other_user.user_id,
                    "name": f"{other_user.first_name} {other_user.last_name}",
                    "pic": other_user.profile_pic or 'default.png'
                })
                
    return jsonify(matches=matches_data), 200


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
    return send_from_directory(app.static_folder, file_dot_text)


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