import os
import urllib.parse
from unittest.mock import patch

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes
from classrank.handlers import _authenticate as auth

test_cookie_secret = "secret_cookie"
static_path = "../classrank/static"
template_path = "../classrank/templates"

class TestSettings(AsyncHTTPTestCase):
    def get_app(self):
        self.settings = {
            "static_path": os.path.join(os.path.dirname(__file__), static_path),
            "template_path": os.path.join(os.path.dirname(__file__), template_path),
            "logged_in_pages": {},
            "logged_out_pages": {},
            "cookie_secret": test_cookie_secret,
            "login_url": "/login"
        }
        cr = ClassRankApp(None, routes, **self.settings)
        with Query(cr.db) as q:
            password = "password"
            h, s = auth.create_password(password)
            q.add(cr.db.account(**{"username": "andrew",
                                   "email_address": "fake@email.com",
                                   "password_hash": h,
                                   "password_salt": s}))
        return cr

    def test_wrong_password(self):
        self.login()
        body = urllib.parse.urlencode({"current_password": "wrongpass",
                                       "new_password": "noupdate",
                                       "new_password_confirm": "noupdate",
                                       "new_email": "no@update.com"})

        with patch('classrank.handlers.BaseHandler.get_current_user') as current_user:
            current_user.return_value = b'"andrew"'
            response = self.fetch("/settings", method="POST", body=body)

            self.assertEqual(response.code, 200)
            self.assertIn(b"Incorrect password", response.body)


    def test_new_password_mismatch(self):
        pass

    def test_new_password_too_short(self):
        pass

    def test_new_email_invalid(self):
        pass

    def test_update_email_success(self):
        pass

    def test_update_password_success(self):
        pass

    def test_update_email_and_password_success(self):
        pass

    def login(self):
        body = urllib.parse.urlencode({"email": "fake@email.com", "password": "password"})
        return self.fetch("/login", method="POST", body=body)


