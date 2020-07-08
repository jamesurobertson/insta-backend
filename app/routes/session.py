from flask import Blueprint, request, jsonify
import jwt
import re

from app.models import db
from app.models.users import User
from app.models.follows import Follow
from ..config import Configuration
from ..auth import require_auth

bp = Blueprint("session", __name__, url_prefix='/api/session')

def checkPassword(password):
    if len(password) < 8:
        return "Password must be 8 characters long"
    elif not re.search('[a-z]', password):
        return "Password must have a lowercase character"
    elif not re.search('[A-Z]', password):
        return "Password must have an uppcase character"
    elif not re.search('[0-9]', password):
        return "Password must have a digit"
    else:
        return True


@bp.route('', methods=["POST"])
def login():
    data = request.json
    if not data['username']:
        return {"error": "Please provide a Username"}, 401
    if not data['password']:
        return{ "error": "Please provide a Password"}, 401
    user = User.query.filter(User.username == data['username']).first()
    if not user:
        return {"error": "Username not found"}, 422

    if user.check_password(data['password']):
        access_token = jwt.encode(
            {'email': user.email}, Configuration.SECRET_KEY)
        return {'access_token': access_token.decode('UTF-8'), 'user': user.to_dict()}
    else:
        return {"error": "Incorrect password"}, 401

@bp.route('/check', methods=["POST"])
def check():
    data=request.json
    try:
        decoded = jwt.decode(data['access_token'], Configuration.SECRET_KEY)

        user = User.query.filter(
            User.email == decoded.get('email')).first()
        num_following = Follow.query.filter(Follow.user_id == user.id).count()
        num_followers = Follow.query.filter(Follow.user_followed_id == user.id).count()
        user_dict = user.to_dict()
        user_dict['numFollowing'] = num_following
        user_dict['numFollowers'] = num_followers
        return {'user': user_dict}
    except:
        return {'error': 'invalid auth token'}, 401

@bp.route('/register', methods=["POST"])
def register():
    data = request.json
    print(data)
    if not data['username']:
        return {"error": 'Please provide a Username'}, 401
    if User.query.filter(User.username == data['username']).first():
        return {"error": 'Username already exists'}, 401
    if not data['email']:
        return {"error": 'Please provide an Email'}, 401
    if User.query.filter(User.email == data['email']).first():
        return {"error": 'Email already exists'}, 401
    if not data['fullName']:
        return {'error': "Please provide your Full Name"}, 401
    if not data['password']:
        return {'error': "Please proivde a Password"}, 401
    if checkPassword(data['password']) != True:
        return {'error': checkPassword(data['password'])}, 401
    if not data['confirmPassword']:
        return {'error': "Please Confirm your Password"}, 401
    if data['password'] != data['confirmPassword']:
        return {'error': "Passwords do not match"}, 401
    
    print(f"\n\n\nDATA\n{data}\n\n\n")
    try:
        user = User(password=data['password'], email=data['email'],
                    full_name=data['fullName'], username=data['username'])
        print(user)
        db.session.add(user)
        db.session.commit()
        access_token=jwt.encode({'email': user.email}, Configuration.SECRET_KEY)
        return {'access_token': access_token.decode('UTF-8'), 'user': user.to_dict()}
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400



@ bp.route('', methods = ["DELETE"])
def logout():
    access_token=jwt.encode({'email': ''}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'user': ''}
