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

            "logged_in_pages": {},

            "logged_out_pages": {},
            "cookie_secret": test_cookie_secret,
            "login_url": "/login"
        }
        cr = ClassRankApp(None, routes, **self.settings)
        with Query(cr.db) as q:
            q.add(cr.db.school(**{"name": "Georgia Institute of Technology",
                                  "abbreviation": "gatech"}))

            q.add(cr.db.course(**{"school_id": 1,
                                  "name": "Machine Learning",
                                  "subject": "CS",
                                  "number": "4641"}))

            q.add(cr.db.section(**{"course_id": 1,
                                   "semester": "spring",
                                   "year": 2016,
                                   "name": "A",
                                   "crn": 1}))
        return cr

    def test_success(self):
        """Test success condition of rating."""
        self.register()
        self.login()
        body = urllib.parse.urlencode({"course": "CS 4641",
                                       "section": "A",
                                       "semester": "spring",
                                       "rating": "5"})
        with patch(get_current_user_func_path) as auth:
            auth.return_value = b'"tester"'
            response = self.fetch("/rate", method="POST", body=body)
            self.assertEqual(self.fetch("/rate").body, response.body)
            with Query(self._app.db) as q:
                rating = q.query(self._app.db.rating).one()
                self.assertEqual(5, rating.rating)

                self.assertEqual("spring", rating.section.semester)
                self.assertEqual(2016, rating.section.year)
                self.assertEqual(1, rating.section.crn)
                self.assertEqual(1, rating.section.course_id)
                self.assertEqual("A", rating.section.name)

                self.assertEqual(1, rating.student.user_id)

    def test_fail_course_not_found(self):
        """Test failure if rating a non-existent course."""
        self.register()
        self.login()
        body = urllib.parse.urlencode({"course": "CS 4150",
                                       "section": "A",
                                       "semester": "spring",
                                       "rating": "5"})
        with patch(get_current_user_func_path) as auth:
            auth.return_value = b'"tester"'
            response = self.fetch("/rate", method="POST", body=body)
            self.assertIn(b"There was an error adding your rating.", response.body)
            with Query(self._app.db) as q:
                rating = q.query(self._app.db.rating).all()
            self.assertEqual(len(rating), 0)

    def test_fail_section_not_found(self):
        """Test failure if rating a non-existent section."""
        self.register()
        self.login()
        body = urllib.parse.urlencode({"course": "CS 4641",
                                       "section": "XXX",
                                       "semester": "spring",
                                       "rating": "5"})
        with patch(get_current_user_func_path) as auth:
            auth.return_value = b'"tester"'
            response = self.fetch("/rate", method="POST", body=body)
            self.assertIn(b"There was an error adding your rating.", response.body)
            with Query(self._app.db) as q:
                rating = q.query(self._app.db.rating).all()
            self.assertEqual(len(rating), 0)

    def test_fail_section_and_course_not_found(self):
        """Test failure if rating a non-existent section and course."""
        self.register()
        self.login()
        body = urllib.parse.urlencode({"name": "MATH-4150",
                                       "section": "XXX",
                                       "semester": "spring",
                                       "rating": "5"})
        with patch(get_current_user_func_path) as auth:
            auth.return_value = b'"tester"'
            response = self.fetch("/rate", method="POST", body=body)
            self.assertIn(b"There was an error adding your rating.", response.body)
            with Query(self._app.db) as q:
                rating = q.query(self._app.db.rating).all()
            self.assertEqual(len(rating), 0)

    def test_fail_invalid_formdata_rating(self):
        """Tests for all types of invalid rating formdata coming in.
        These should be detected by the RateForm validator. The invalid types
        are:
            1. rating too high (> 5),
            2. rating too low  (< 1),
            3. rating not extant,
            4. name too short (< 5),
            5. name too long  (> 30),
            6. name not extant,
            7. section name too short / not extant, and
            8. section name too long (> 4).

        In each case, we want to go back to a blank 'rate' page. Finally, we
        then wish to assert that nothing was added to the database from these
        attempts.
        """
        self.register()
        rate_body = self.fetch("/rate").body

        invalid_forms = [
            {"name": "CS-4641", "section": "A",
             "semester": "spring", "rating": "6"},

            {"name": "CS-4641", "section": "A",
             "semester": "spring", "rating": "0"},

            {"name": "CS-4641", "section": "A",
             "semester": "spring", "rating": ""},

            {"name": "C", "section": "A",
             "semester": "spring", "rating": "3"},

            {"name": "CS-0123456789abcdefghijklmnopqr", "section": "A",
             "semester": "spring ", "rating": "3"},

            {"name": "", "section": "A",
             "semester": "spring", "rating": "3"},

            {"name": "CS-4641", "section": "",
             "semester": "spring", "rating": "3"},

            {"name": "CS-4641", "section": "A 123456789",
             "semester": "spring", "rating": "3"}
        ]
        # iterate over all forms, returning to register page each time
        for form in invalid_forms:
            response = self.post_form(form)
            self.assertIn(b"There was an error adding your rating.", response.body)

        # assert that nothing was added to database from all attempts
        with Query(self._app.db) as q:
            rating = q.query(self._app.db.rating).all()
            self.assertEqual(0, len(rating))

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

    def post_form(self, formdata, to_page="/rate"):
        body = urllib.parse.urlencode(formdata)
        return self.fetch(to_page, method="POST", body=body)
