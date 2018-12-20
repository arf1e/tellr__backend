from unittest import TestCase
from tellr import app
from tellr.db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        # make sure db exists
        with app.app_context():
            db.create_all()
        # get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # db is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
