import os
import boto3
import time
from flask import Blueprint, request
from ..models import db
from ..models.users import User

bp = Blueprint("aws", __name__, url_prefix="/api/aws")

UPLOAD_FOLDER = 'uploads'
BUCKET = 'slickpics'


@bp.route('/<id>', methods=["POST"])
def upload(id):
    if request.method == "POST":
        f = request.files['file']
        f.filename = change_name(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"uploads/{f.filename}", BUCKET)
        user = User.query.filter(User.id == id).first()
        user.profile_image_url = f'https://slickpics.s3.us-east-2.amazonaws.com/uploads/{f.filename}'
        db.session.commit()
        return {"img": f'https://slickpics.s3.us-east-2.amazonaws.com/uploads/{f.filename}'}


@bp.route('/post/<currentUserId>/<content>', methods=["POST"])
def upload_post(currentUserId, content):
    print(request.files)
    f = request.files['file']
    f.filename = change_name(f.filename)
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    upload_file(f"uploads/{f.filename}", BUCKET)
    image_url = f'https://slickpics.s3.us-east-2.amazonaws.com/uploads/{f.filename}'

    try:
        post= Post(user_id=data['currentUserId'], image_url=image_url, caption=data['caption'])
        db.session.add(post)
        db.session.commit()
        post_dict = post.to_dict()
        return post_dict
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400

    return {"img": f'https://slickpics.s3.us-east-2.amazonaws.com/uploads/{f.filename}'}


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response


def change_name(file_name):
    return f"{time.ctime().replace(' ', '').replace(':', '')}.png"
