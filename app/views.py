from app import app, db
from sqlalchemy import or_
from .models import User, Profile, Match, Message
from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
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
    email = request.form.get('email', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not email or not username or not password:
        return jsonify({"errors": ["Email, username, and password are required"]}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"errors": ["Email already registered"]}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"errors": ["Username already taken"]}), 400

    filename = "default.png"
    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    try:
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            first_name=request.form.get('first_name', 'New'),
            last_name=request.form.get('last_name', 'User'),
            age=request.form.get('age', type=int),
            gender=request.form.get('gender'),
            location=request.form.get('location', 'Unknown'),
            bio=request.form.get('bio', ''),
            hobbie1=request.form.get('hobbie1', ''),
            hobbie2=request.form.get('hobbie2', ''),
            hobbie3=request.form.get('hobbie3', ''),
            relationship_goal=request.form.get('relationship_goal', ''),
            profile_pic=filename,
            visibility=request.form.get('visibility', 'public')
        )
        db.session.add(profile)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500

   
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

    interacted_ids = [m.target_id for m in Match.query.filter_by(user_id=current_user_id).all()]
    interacted_ids.append(int(current_user_id))

    query = Profile.query.filter(
        ~Profile.user_id.in_(interacted_ids),
        Profile.visibility == 'public'
    )

    search = request.args.get('search', '').strip()
    if search:
        pattern = f'%{search}%'
        query = query.filter(
            or_(
                Profile.first_name.ilike(pattern),
                Profile.last_name.ilike(pattern),
                Profile.bio.ilike(pattern)
            )
        )

    location = request.args.get('location', '').strip()
    if location:
        query = query.filter(Profile.location.ilike(f'%{location}%'))

    min_age = request.args.get('min_age', type=int)
    max_age = request.args.get('max_age', type=int)
    if min_age:
        query = query.filter(Profile.age >= min_age)
    if max_age:
        query = query.filter(Profile.age <= max_age)

    interest = request.args.get('interest', '').strip()
    if interest:
        pattern = f'%{interest}%'
        query = query.filter(
            or_(
                Profile.hobbie1.ilike(pattern),
                Profile.hobbie2.ilike(pattern),
                Profile.hobbie3.ilike(pattern)
            )
        )

    sort = request.args.get('sort', 'newest')
    query = query.order_by(Profile.join_date.asc() if sort == 'oldest' else Profile.join_date.desc())

    profiles = query.all()
    return jsonify(profiles=[{
        "id": p.user_id,
        "name": f"{p.first_name} {p.last_name}",
        "age": p.age,
        "location": p.location,
        "bio": p.bio,
        "hobbie1": p.hobbie1,
        "hobbie2": p.hobbie2,
        "hobbie3": p.hobbie3,
        "pic": p.profile_pic
    } for p in profiles])


@api.route('/like', methods=['POST'])
@jwt_required()
def like_user():
    current_user_id = get_jwt_identity()
    target_id = request.json.get('target_id')
    action = request.json.get('action', 'like')  # 'like' or 'pass'

    new_match = Match(user_id=current_user_id, target_id=target_id, status=action)
    db.session.add(new_match)
    db.session.commit()

    is_match = False
    if action == 'like':
        mutual = Match.query.filter_by(user_id=target_id, target_id=current_user_id, status='like').first()
        is_match = bool(mutual)

    return jsonify(is_match=is_match)


@api.route('/profile', methods=['GET'])
@jwt_required()
def get_my_profile():
    current_user_id = get_jwt_identity()

    user = db.session.get(User, int(current_user_id))
    profile = Profile.query.filter_by(user_id=current_user_id).first()

    if not user or not profile:
        return jsonify(error="Profile not found"), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "age": profile.age,
        "gender": profile.gender,
        "location": profile.location,
        "bio": profile.bio,
        "hobbie1": profile.hobbie1,
        "hobbie2": profile.hobbie2,
        "hobbie3": profile.hobbie3,
        "relationship_goal": profile.relationship_goal,
        "visibility": profile.visibility,
        "pic": profile.profile_pic or 'default.png'
    }), 200


@api.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    profile = Profile.query.filter_by(user_id=current_user_id).first()

    if not profile:
        return jsonify(error="Profile not found"), 404

    if 'profile_pic' in request.files:
        file = request.files['profile_pic']
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile.profile_pic = filename

    profile.first_name = request.form.get('first_name', profile.first_name)
    profile.last_name = request.form.get('last_name', profile.last_name)
    profile.bio = request.form.get('bio', profile.bio)
    profile.location = request.form.get('location', profile.location)
    profile.hobbie1 = request.form.get('hobbie1', profile.hobbie1)
    profile.hobbie2 = request.form.get('hobbie2', profile.hobbie2)
    profile.hobbie3 = request.form.get('hobbie3', profile.hobbie3)
    profile.relationship_goal = request.form.get('relationship_goal', profile.relationship_goal)
    profile.visibility = request.form.get('visibility', profile.visibility)

    age = request.form.get('age', type=int)
    if age:
        profile.age = age
    gender = request.form.get('gender')
    if gender:
        profile.gender = gender

    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200


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
                    "bio": other_user.bio or '',
                    "pic": other_user.profile_pic or 'default.png'
                })
                
    return jsonify(matches=matches_data), 200


@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return jsonify(error="User not found"), 404
    return jsonify({
        "user_id": user_id,
        "name": f"{profile.first_name} {profile.last_name}",
        "pic": profile.profile_pic or 'default.png',
        "bio": profile.bio or ''
    }), 200


@api.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    current_user_id = int(get_jwt_identity())

    msgs = Message.query.filter(
        (Message.sender_id == current_user_id) | (Message.recipient_id == current_user_id)
    ).order_by(Message.timestamp.desc()).all()

    seen = set()
    conversations = []
    for msg in msgs:
        other_id = msg.recipient_id if msg.sender_id == current_user_id else msg.sender_id
        if other_id not in seen:
            seen.add(other_id)
            profile = Profile.query.filter_by(user_id=other_id).first()
            if profile:
                conversations.append({
                    "user_id": other_id,
                    "name": f"{profile.first_name} {profile.last_name}",
                    "pic": profile.profile_pic or 'default.png',
                    "last_message": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })

    return jsonify(conversations=conversations), 200


@api.route('/messages/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_messages(other_user_id):
    current_user_id = int(get_jwt_identity())

    msgs = Message.query.filter(
        ((Message.sender_id == current_user_id) & (Message.recipient_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.recipient_id == current_user_id))
    ).order_by(Message.timestamp.asc()).all()

    return jsonify(messages=[{
        "id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
        "timestamp": m.timestamp.isoformat(),
        "is_mine": m.sender_id == current_user_id
    } for m in msgs]), 200


@api.route('/messages/<int:other_user_id>', methods=['POST'])
@jwt_required()
def send_message(other_user_id):
    current_user_id = int(get_jwt_identity())

    i_liked = Match.query.filter_by(user_id=current_user_id, target_id=other_user_id, status='like').first()
    they_liked = Match.query.filter_by(user_id=other_user_id, target_id=current_user_id, status='like').first()

    if not i_liked or not they_liked:
        return jsonify(error="You can only message mutual matches"), 403

    data = request.get_json()
    content = (data.get('content') or '').strip()
    if not content:
        return jsonify(error="Message cannot be empty"), 400

    message = Message(sender_id=current_user_id, recipient_id=other_user_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({
        "id": message.id,
        "sender_id": message.sender_id,
        "content": message.content,
        "timestamp": message.timestamp.isoformat(),
        "is_mine": True
    }), 201


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