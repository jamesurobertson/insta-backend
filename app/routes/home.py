from flask import Blueprint, request, jsonify

bp = Blueprint("home", __name__, url_prefix='')


@bp.route('/')
def home():
    return 'hello!! eshahhe'
