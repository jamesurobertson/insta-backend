from flask import Blueprint, request
from sqlalchemy.orm import joinedload
from urllib import parse
from ..models import db
from ..models.posts import Post
from ..models.users import User
from ..models.follows import Follow
from ..models.likes import Like
from ..models.comments import Comment
from ..auth import require_auth

bp = Blueprint("query", __name__, url_prefix="/api/search")


@bp.route('')
def query():
    query = request.args.get('query')
    print(query)

    userResults = User.query.filter(User.username.ilike(f'%{query}%')).all()
    print(userResults)

    results = []
    
    for user in userResults:
        user_dict = user.to_dict()
        results.append(user_dict)

    return {"results": results}


