from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.users import User
from ..models.follows import Follow
from ..auth import require_auth

#  following = /:id/following
#  follows = /:id

bp = Blueprint("follow", __name__, url_prefix="/api/follow")

# users who follow user of <id>
@bp.route('/<id>')
def getFollows(id):
    follows = Follow.query.filter(Follow.user_followed_id == id).all()

    followsList = []
    for user in follows:
        print(user)
        followsList.append(user.to_dict())
    return {"users": followsList}
