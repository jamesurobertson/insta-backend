from flask import Blueprint, request
from sqlalchemy.orm import joinedload
from ..models import db
from ..models.users import User
from ..auth import require_auth

bp = Blueprint("users", __name__, url_prefix="/api/user")

@bp.route('/')
@require_auth
def index():
