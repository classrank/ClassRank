import os
import urllib.parse
from unittest.mock import patch

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes
from test import create_test_database

test_cookie_secret = "secret_cookie"


class TestApplication(AsyncHTTPTestCase):
    def get_app(self):
        self.settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "../classrank/static"),
            "template_path": os.path.join(os.path.dirname(__file__),
                                          "../classrank/templates"),
            "logged_in_pages": {},
            "logged_out_pages": {},
            "cookie_secret": test_cookie_secret,
            "login_url": "/login"
        }
        cr = ClassRankApp(os.environ.get("CONNECTION", "sqlite://"), routes, **self.settings)
        with Query(cr.db) as q:
            q.add(cr.db.school(**{"name":"Georgia Test University", "abbreviation": "test"}))
        return cr

    def test_db_example(self):
        with Query(self._app.db) as q:
            q.session.delete(q.query(self._app.db.school).one())
        create_test_database(self._app)

    def test_splash(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        print(self.get_url("/"))
        self.assertIn("ClassRank".encode('utf-8'), response.body)

    def test_login_get(self):
        response = self.fetch("/login")
        self.assertEqual(response.code, 200)

    def test_register_get(self):
        response = self.fetch("/register")
        self.assertEqual(response.code, 200)

    def test_login_post_fail(self):
        body = urllib.parse.urlencode({"email": "test@test.com", "password": "secret"})
        response = self.fetch("/login", method="POST", body=body)
        self.assertIn(b"No user exists with that email address", response.body)

    def test_register_post_fail(self):
        body = urllib.parse.urlencode({"email": "test@test.com", "school": "test",
                                       "username": "t", "password": "password",
                                       "password_confirm": "password"})
        response = self.fetch("/register", method="POST", body=body)
        self.assertIn(b"Username must be 3-25 characters", response.body)

    def test_register_post_success(self):
        body = urllib.parse.urlencode({"email": "test@test.com", "school": "test",
                                       "username": "tester", "password": "password",
                                       "password_confirm": "password"})
        response = self.fetch("/register", method="POST", body=body)
        self.assertEqual(self.fetch("/login").body, response.body)
        with Query(self._app.db) as q:
            user = q.query(self._app.db.account).one()
            self.assertEqual("test@test.com", user.email_address)

    def test_register_existing_user(self):
        self.create_example_user()
        body = urllib.parse.urlencode({"email": "test@test.com", "school": "test",
                                       "username": "tester", "password": "password",
                                       "password_confirm": "password"})
        response = self.fetch("/register", method="POST", body=body)

        self.assertIn(b"A user with that username or email address already exists, or invalid school", response.body)

    def test_login_post_success(self):
        hash_pass, response = self.login()

        self.assertIn(b"Welcome to ClassRank!", response.body)
        self.assertEqual(("password", b"salt"), hash_pass.call_args[0])

    def test_logout(self):
        self.login()

        with patch('classrank.handlers.BaseHandler.get_current_user') as auth:
            auth.return_value = "tester"
            response = self.fetch("/logout", method="GET")

        self.assertIn("ClassRank".encode('utf-8'), response.body)

    def create_example_user(self):
        """
        Add's a user to the database and creates corresponding login headers

        :return: the HTTP headers corresponding to the user's data
        """
        body = urllib.parse.urlencode({"email": "test@test.com", "password": "password"})
        user = self._app.db.account(username="tester", email_address="test@test.com",
                                    password_hash=b"secret", password_salt=b"salt")

        with Query(self._app.db) as db:
            db.add(user)

        return body

    def login(self):
        body = self.create_example_user()

        with patch('classrank.handlers._authenticate.hash_pw') as hash_pass:
            with patch(
                    'classrank.handlers.BaseHandler.get_current_user') as authenticator:
                authenticator.return_value = "tester"
                hash_pass.return_value = b"secret"

                return hash_pass, self.fetch("/login", method="POST", body=body)

    def tearDown(self):
        self._app.db.metadata.bind = self._app.db.engine
        self._app.db.metadata.drop_all()
