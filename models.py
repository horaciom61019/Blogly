"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

def connect_db(app):
    """ Connect to database """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User data model  """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False, unique=True)
    last_name = db.Column(db.Text, nullable=False, unique=True)
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