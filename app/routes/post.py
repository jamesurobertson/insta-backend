from flask import Blueprint, request
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.posts import Post
from ..models.users import User
from ..models.follows import Follow
from ..models.likes import Like
from ..models.comments import Comment
from ..auth import require_auth

bp = Blueprint("posts", __name__, url_prefix="/api/post")


@bp.route('/')
def index():
    post_list = []
    posts = Post.query.all()
    for post in posts:
        post_list.append(post.to_dict())
    return {"posts": post_list}
