from flask import Blueprint, request
from ..models import db
from ..models.comments import Comment
from ..models.users import User
from ..models.likes import Like

bp = Blueprint("comment", __name__, url_prefix="/api/comment")


@bp.route('', methods=["POST"])
def postComment():
    data = request.json
    print(data)
    comment = Comment(user_id=data['userId'], post_id=data['postId'], content=data['content'])
    comment_dict = comment.to_dict()
    print(comment_dict)
    db.session.add(comment)
    db.session.commit()
    user = User.query.filter(User.id == comment.user_id).first()
    likes = Like.query.filter(Like.likeable_id == comment.id).filter(Like.likeable_type == 'comment').all()
    likes_comment = []

    for like in likes:
        likes_comment.append(like.to_dict())
    comment_dict['likes_comment'] = likes_comment
    comment_dict["username"] = user.to_dict()
    return comment_dict
