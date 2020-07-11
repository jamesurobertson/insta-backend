from flask import Blueprint, request
from ..models import db
from ..models.comments import Comment

bp = Blueprint("comment", __name__, url_prefix="/api/comment")


@bp.route('', methods=["POST"])
def postComment():
    data = request.json
    print(data)
    comment = Comment(user_id=data['userId'], post_id=data['postId'], content=data['content'])
    db.session.add(comment)
    db.session.commit()

    return comment.to_dict()
