from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.users import User
from ..models.likes import Like
from ..auth import require_auth


bp = Blueprint("like", __name__, url_prefix="/api/like")


@bp.route('/<likeableType>/<id>')
def getLikes(likeableType, id):
    likes = Like.query.filter(
        Like.likeable_id == id).filter(Like.likeable_type == likeableType).all()

    likesList = []
    for like in likes:
        user = User.query.filter(Like.user_id == User.id).first()
        likesList.append(user.to_dict())
    return {"users": likesList}


@bp.route('', methods=["POST"])
def post_like():
    data = request.json
    print(data)

    like = Like(user_id=data["userId"], likeable_id=data["id"], likeable_type=data["likeableType"])
    user = User.query.filter(User.id == data["userId"]).first()
    db.session.add(like)
    db.session.commit()

    return user.to_dict()

@bp.route('', methods=["DELETE"])
def delete_like():
    data = request.json
    print(data)
    like = Like.query.filter(Like.user_id == data["userId"]).filter(Like.likeable_id == data["id"]).filter(Like.likeable_type == data["likeableType"]).first()
    print(like)
    user = like.user
    db.session.delete(like)
    db.session.commit()

    return user.to_dict()
