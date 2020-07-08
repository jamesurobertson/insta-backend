from flask import Blueprint, request, jsonify
import jwt

from app.models import db
from app.models.users import User
from ..config import Configuration
from ..auth import require_auth

bp = Blueprint("session", __name__, url_prefix='/api/session')


@bp.route('', methods=["POST"])
def login():
    data = request.json
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
        return {'user': user.to_dict()}
    except:
        return {'error': 'invalid auth token'}, 401

@bp.route('/register', methods=["POST"])
def register():
    data = request.json
    print(f"\n\n\nDATA\n{data}\n\n\n")
    user = User(birthday=data['birthday'], password=data['password'], email=data['email'],
                full_name=data['fullName'], username=data['username'])
    print(user)
    db.session.add(user)
    db.session.commit()

    access_token=jwt.encode({'email': user.email}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'user': user.to_dict()}


@ bp.route('', methods = ["DELETE"])
def logout():
    access_token=jwt.encode({'email': ''}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'user': ''}
