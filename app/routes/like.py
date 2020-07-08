from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.users import User
from ..models.likes import Like
from ..auth import require_auth

#  likes = /:type/:id

bp = Blueprint("like", __name__, url_prefix="/api/like")

# users who follow user of <id>


@bp.route('/<likeableType>/<id>')
def getFollows(likeableType, id):
    likes = Like.query.filter(
        Like.likeable_id == id).filter(Like.likeable_type == likeableType).all()

    likesList = []
    for like in likes:
        user = User.query.filter(Like.user_id == User.id).first()
        likesList.append(user.to_dict())
    return {"users": likesList}
