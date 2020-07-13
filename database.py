import secrets

from app.models.comments import Comment
from app.models.saved_posts import Saved_Post
from app.models.posts import Post
from app.models.likes import Like
from app.models.follows import Follow
from app.models.users import User
from app import app, db
from faker import Faker
from random import *
from dotenv import load_dotenv
load_dotenv()


fake = Faker()

# Regardless of the lint error you receive,
# load_dotenv must run before running this
# so that the environment variables are
# properly loaded.

defaultPic = 'https://slickpics.s3.us-east-2.amazonaws.com/uploads/SunJul122059252020.png'

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(full_name="James Robertson", username="jamesurobertson",
             password="Test@1234", email='jamesurobertson@gmail.com',
             profile_image_url=defaultPic),
        User(full_name="Zachary Henderson", username="crocs93",
             password="Test@1234", email='zachary.henderson114@gmail.com',
             profile_image_url=defaultPic),
        User(full_name="Aaron Pierskalla", username="aaron_the_king",
             password="Test@1234", email='ajpierskalla3@gmail.com',
             profile_image_url=defaultPic)
    ]
    for i in range(1,50):
        name = fake.name()
        username = f"{name.replace(' ', '')}{randint(1,1000)}"
        email = f'{username}@isntgram.com'

        user = User(full_name=name, username=username, password='Test@1234',
                    email=email, profile_image_url=defaultPic, bio=fake.text())
        users.append(user)

    follows = []
    for i in range(1,50):
        followsNum = randint(30, 40)
        followed_set = set()
        while len(followed_set) < followsNum:
            followed_user_id = randint(1, 50)
            if followed_user_id == i:
                continue
            followed_set.add(followed_user_id)
        for j in followed_set:
            follows.append(Follow(user_id=i, user_followed_id=j))


    posts = []

    for i in range(1, 50):
        num_posts = randint(10, 20)
        for j in range(1, num_posts):
            randint(1, 1000000)
            image = f'https://picsum.photos/seed/{secrets.token_hex(10)}/1000/1000'
            posts.append(Post(user_id=i, caption=fake.text(), image_url=image))


    comments = []

    for i in range(1, 50):
        comment_count = randint(10, 40)
        for j in range(1, comment_count):
            postId = randint(1, len(posts))
            comments.append(Comment(user_id=i, content=fake.text(), post_id=postId))

    likes = []

    for i in range(1, 658):
        users_liked_set = set()
        like_post_count = randint(0, 15)
        while len(users_liked_set) < like_post_count:
            userId = randint(1, len(users))
            if userId in users_liked_set:
                continue
            likes.append(Like(user_id=userId, likeable_id=i, likeable_type='post'))
            users_liked_set.add(userId)

    for user in users:
        db.session.add(user)

    for post in posts:
        db.session.add(post)

    for like in likes:
        db.session.add(like)

    for comment in comments:
        db.session.add(comment)

    for follow in follows:
        db.session.add(follow)

    db.session.commit()
