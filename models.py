"""Models for Blogly."""

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


###################################### PART TWO - Adding Posts ####################################

class Post(db.Model):
    """ Post data model  """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # a foreign key to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


################################# PART THREE - Add M2M Relationship ################################

class Tag(db.Model):
    """ Tag data model - can be added to posts """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

class PostTag(db.Model):
    """ Tag on a post """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

