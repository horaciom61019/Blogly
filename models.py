"""Models for Blogly."""

from turtle import title
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User data model  """

    __tablename__ = "users"

    posts = db.relationship("Post", backref="user")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    ''' 
    @property decorator makes usage of getter and setters much easier in Object-Oriented Programming.
    Without @property:  Test01 Test01
    With @property: <bound method User.full_name of <User 1>>
    '''
    @property
    def full_name(self):
        """ Returns user's full name """

        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    """ Post data model  """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # a foreign key to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    