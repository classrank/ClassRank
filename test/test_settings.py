import os
import urllib.parse
from unittest.mock import patch

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes

test_cookie_secret = "secret_cookie"

class TestSettings(AsyncHTTPTestCase):
    def get_app(self):
        self.settings = {
            "static_path": path.join(path.dirname(__file__), static_path),
            "template_path": path.join(path.dirname(__file__), template_path),

            "logged_in_pages": ["dashboard", "search", "rate",
                                "privacy", "settings", "logout"],

            "logged_out_pages": ["login", "register"],
            "cookie_secret": test_cookie_secret,
            "login_url": "/login"
        }
        cr = ClassRankApp(None, routes, **self.settings)
        with Query(cr.db) as q:
            q.add(cr.db.school(**{"name": "Georgia Institute of Technology",
                                  "abbreviation": "gatech"}))

            q.add(cr.db.course(**{"school_id": 1,
                                  "name": "Machine Learning",
                                  "abbreviation": "CS-4641"}))

            q.add(cr.db.section(**{"course_id": 1,
                                   "semester": "spring",
                                   "year": 2016,
                                   "name": "A",
                                   "crn": 1}))
        return cr

    def test_wrong_password(self):

    def test_new_password_mismatch(self):

    def test_new_password_too_short(self):

    def test_new_email_invalid(self):

    def test_update_email_success(self):

    def test_update_password_success(self):

    def test_update_email_and_password_success(self):


