from msilib.schema import Class
from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db' 
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """ Test model for Users """

    def setUp(self) -> None:
        """ Clean up any existing users """
        
        User.query.delete()

    def tearDown(self):
        """ Clean up any fouled transaction """

        db.session.rollback()

    def test_full_name(self):
        full_name = User( first_name="First01", last_name="Last01", image_url=None)
        self.assertEqual(full_name.full_name, "First01 Last01")