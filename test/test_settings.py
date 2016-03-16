from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes
from os import path
from tornado.testing import AsyncHTTPTestCase
import urllib.parse
from unittest.mock import patch

"""Tests the 'add ratings' function of ClassRank."""

test_cookie_secret = "secret_cookie"
static_path = "../classrank/static"
template_path = "../classrank/templates"

# path to the function 'get_current_user'; for patching purposes
get_current_user_func_path = "classrank.handlers.BaseHandler.get_current_user"


class TestRatings(AsyncHTTPTestCase):
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
        self.register()
        meh, response = self.login()
        self.assertEqual(response.code, 200)

        # body = urllib.parse.urlencode({"current_password": "wrongpass",
        #                                "new_password": "noupdate",
        #                                "new_password_confirm": "noupdate",
        #                                "new_email": "no@update.com"})

      
        # response = self.fetch("/settings")
        # self.assertEqual(response.code, 200)

        # response = self.fetch("/settings", method="POST", body=body)

        # self.assertEqual(response.code, 200)
        # self.assertIn(b"Incorrect password", response.body)

    def register(self):
        body = urllib.parse.urlencode({"email": "test@test.com",
                                       "school": "gatech",
                                       "username": "tester",
                                       "password": "password",
                                       "password_confirm": "password"})
        response = self.fetch("/register", method="POST", body=body)

    def login(self):
        body = urllib.parse.urlencode({"email": "test@test.com",
                                       "password": "password"})

        with patch('classrank.handlers._authenticate.hash_pw') as passhash:
            with patch(get_current_user_func_path) as auth:
                auth.return_value = "tester"
                passhash.return_value = "secret"

                return passhash, self.fetch("/login", method="POST", body=body)


# import os
# import urllib.parse
# from unittest.mock import patch

# from tornado.testing import AsyncHTTPTestCase

# from classrank.app import ClassRankApp
# from classrank.database.wrapper import Query
# from classrank.routing import routes
# from classrank.handlers import _authenticate as auth

# test_cookie_secret = "secret_cookie"
# static_path = "../classrank/static"
# template_path = "../classrank/templates"

# class TestSettings(AsyncHTTPTestCase):
#     def get_app(self):
#         self.settings = {
#             "static_path": os.path.join(os.path.dirname(__file__), static_path),
#             "template_path": os.path.join(os.path.dirname(__file__), template_path),

#             "logged_in_pages": ["dashboard", "search", "rate",
#                                 "privacy", "settings", "logout"],

#             "logged_out_pages": ["login", "register"],
#             "cookie_secret": test_cookie_secret,
#             "login_url": "/login"
#         }
#         cr = ClassRankApp(None, routes, **self.settings)
#         with Query(cr.db) as q:
#             password = "password"
#             h, s = auth.create_password(password)
#             q.add(cr.db.account(**{"username": "andrew",
#                                    "email_address": "fake@email.com",
#                                    "password_hash": h,
#                                    "password_salt": s}))
#         return cr


#     def test_new_password_mismatch(self):
#         pass

#     def test_new_password_too_short(self):
#         pass

#     def test_new_email_invalid(self):
#         pass

#     def test_update_email_success(self):
#         pass

#     def test_update_password_success(self):
#         pass

#     def test_update_email_and_password_success(self):
#         pass

#     def login(self):
#         body = urllib.parse.urlencode({"email": "fake@email.com", "password": "password"})
#         return self.fetch("/login", method="POST", body=body)


