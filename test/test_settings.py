import os
import urllib.parse
from unittest.mock import patch

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes
from classrank.handlers import _authenticate as authenticate

test_cookie_secret = "secret_cookie"


class TestApplication(AsyncHTTPTestCase):
    def get_app(self):
        self.settings = {
            "logged_in_pages": {},
            "logged_out_pages": {},
            "static_path": os.path.join(os.path.dirname(__file__), "../classrank/static"),
            "template_path": os.path.join(os.path.dirname(__file__),
                                          "../classrank/templates"),
            "cookie_secret": test_cookie_secret,
            "login_url": "/login"
        }
        cr = ClassRankApp(None, routes, **self.settings)
        with Query(cr.db) as q:
            q.add(cr.db.school(**{"name":"Georgia Test University", "abbreviation": "test"}))
            phash, psalt = authenticate.create_password("password")
            q.add(cr.db.account(username="andrew", email_address="my@mail.com", password_hash=phash,
                          password_salt=psalt))

        return cr

    def test_wrong_password(self):
        body = urllib.parse.urlencode({"current_password": "wrongpass",
                                       "new_password": "noupdate",
                                       "new_password_confirm": "noupdate",
                                       "new_email": "no@update.com"})

      
        with patch('classrank.handlers.BaseHandler.get_current_user') as get_current_user:
            get_current_user.return_value = b'"andrew"'
            response = self.fetch("/settings", method="POST", body=body)

            self.assertEqual(response.code, 200)
            self.assertIn(b"Incorrect password", response.body)

    def test_mismatch_new_passwords(self):
        body = urllib.parse.urlencode({"current_password": "password",
                                       "new_password": "purple",
                                       "new_password_confirm": "orange",
                                       "new_email": "no@update.com"})

      
        with patch('classrank.handlers.BaseHandler.get_current_user') as get_current_user:
            get_current_user.return_value = b'"andrew"'
            response = self.fetch("/settings", method="POST", body=body)

            self.assertEqual(response.code, 200)
            self.assertIn(b"Passwords did not match", response.body)

            with Query(self._app.db) as q:
                user = q.query(self._app.db.account).filter_by(username="andrew").one()
                self.assertEqual(user.password_hash, authenticate.hash_pw("password", user.password_salt))

                # Did not update.. Even though entering new email wasn't erroneous, either ALL
                # updates should go through or NONE. Since new passwords didn't match, NO
                # updates should go through, so don't update email.
                self.assertEqual(user.email_address, "my@mail.com")

    def test_update_email_only(self):
        body = urllib.parse.urlencode({"current_password": "password",
                                       "new_password": "",
                                       "new_password_confirm": "",
                                       "new_email": "yes@update.com"})

      
        with patch('classrank.handlers.BaseHandler.get_current_user') as get_current_user:
            get_current_user.return_value = b'"andrew"'
            response = self.fetch("/settings", method="POST", body=body)

            self.assertEqual(response.code, 200)
            self.assertIn(b"Your information has been updated", response.body)

            with Query(self._app.db) as q:
                user = q.query(self._app.db.account).filter_by(username="andrew").one()
                self.assertEqual(user.password_hash, authenticate.hash_pw("password", user.password_salt))
                self.assertEqual(user.email_address, "yes@update.com")

    '''Not necessary (actually, more like impossible) to test updating ONLY password.
    The password update is optional, but the POST will ALWAYS update the email,
    since the email form auto-fills with the current email. If the user doesn't
    want to change their email, they just don't mess with that form, but the
    logic still "updates" the email to the same email that it already is. Thus,
    if email AND password update works, it goes without saying that just updating
    ones password works'''
    def test_update_email_and_password(self):
        body = urllib.parse.urlencode({"current_password": "password",
                                       "new_password": "newpass",
                                       "new_password_confirm": "newpass",
                                       "new_email": "yes@update.com"})

      
        with patch('classrank.handlers.BaseHandler.get_current_user') as get_current_user:
            get_current_user.return_value = b'"andrew"'
            response = self.fetch("/settings", method="POST", body=body)

            self.assertEqual(response.code, 200)
            self.assertIn(b"Your information has been updated", response.body)

            with Query(self._app.db) as q:
                user = q.query(self._app.db.account).filter_by(username="andrew").one()
                self.assertEqual(user.password_hash, authenticate.hash_pw("newpass", user.password_salt))
                self.assertEqual(user.email_address, "yes@update.com")


