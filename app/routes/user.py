from flask import Blueprint, request
from sqlalchemy.orm import joinedload
from ..models import db
from ..config import Configuration

from ..models.users import User
from ..auth import require_auth
import jwt

bp = Blueprint("users", __name__, url_prefix="/api/user")

@bp.route('', methods=['PUT'])
def update_user():
    data = request.json
    user = User.query.filter(User.id == data["id"]).first()
    old_user = user.to_dict()
    if user.username != data["username"]:
        if User.query.filter(User.username == data['username']).first():
            return {"error": 'Username already exists'}, 401
        user.username = data["username"]
    if user.email != data["email"]:
        if User.query.filter(User.email == data['email']).first():
            return {"error": 'Email already exists'}, 401
        user.email = data["email"]
    if user.full_name != data["fullName"]:
        user.full_name = data["fullName"]
    if user.bio != data["bio"]:
        user.bio = data["bio"]
    db.session.commit()

    old_keys = set(old_user.values())
    new_keys = set(user.to_dict().values())

    print(len(old_keys.intersection(new_keys)))
    print(len(old_keys.intersection(new_keys)))
    if len(old_keys.intersection(new_keys)) == 6:
        return {"error": "No changes made"}, 401

    access_token = jwt.encode({'email': user.email}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'user': user.to_dict()}
