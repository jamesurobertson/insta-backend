from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.posts import Post
from ..models.users import User
from ..models.follows import Follow
from ..models.likes import Like
from ..models.comments import Comment
from ..auth import require_auth

bp = Blueprint("profile", __name__, url_prefix="/api/profile")


@bp.route('/<id>')
def index(id):
    post_count = Post.query.filter(Post.user_id == id).count()
    followers = Follow.query.filter(Follow.user_followed_id == id).all()
    follows = Follow.query.filter(Follow.user_id == id).all()
    user = User.query.filter(User.id == id).first()
    posts = Post.query.filter(Post.user_id == id).all()
    plist = []

    followersList = []
    followsList = []

    for follower in followers:
        followersList.append(follower.to_dict())

    for follower in follows:
        followsList.append(follower.to_dict())

    for post in posts:
        post_dict = post.to_dict()
        print(post_dict)
        likes = Like.query.filter(Like.likeable_id == post_dict["id"] and Likes.likeableType == 'post').count()
        comments = Comment.query.filter(Comment.post_id == post_dict["id"]).count()
        post_dict["like_count"] = likes
        post_dict["comment_count"] = comments
        plist.append(post_dict)
    return {"num_posts": post_count, "posts": plist, "followersList": followersList, "followsList": followsList, "user": user.to_dict() }
