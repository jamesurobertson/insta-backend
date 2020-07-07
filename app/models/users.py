from ..models import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    profile_image_url = db.Column(db.String(255))
    bio = db.Column(db.String(2000))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(), onupdate=func.now(),
                           nullable=False)

    posts = db.relationship("Post", back_populates="user")
    follows = db.relationship("Follow", back_populates="user")
    messages = db.relationship("Message", back_populates="user")
    likes = db.relationship("Like", back_populates="user")
    saved = db.relationship("Saved_Post", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    user_conversations = (db.relationship("User_Conversation",
                                          back_populates="user"))

    @property
    def password(self):
        return hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email, "full_name": self.full_name, "username": self.username,
                "profile_image_url": self.profile_image_url,
                "bio": self.bio}
