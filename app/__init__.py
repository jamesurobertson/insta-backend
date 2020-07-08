from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.config import Configuration
from app.routes import session, profile, follow, like
from app.models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(session.bp)
<<<<<<< HEAD
# app.register_blueprint(post.bp)
=======
app.register_blueprint(profile.bp)
app.register_blueprint(follow.bp)
app.register_blueprint(like.bp)
>>>>>>> 42089aade5fcc4264e3987cd88864fe8fcf62d85
