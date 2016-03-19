import os

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.database.wrapper import Query
from classrank.routing import routes
import json

test_cookie_secret = "secret_cookie"

class TestApiHandlers(AsyncHTTPTestCase):
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
            q.add(cr.db.course(**{"school_id": 1, "name": "CS-4641", "description": "Machine learning", "number": "4641", "subject": "CS"}))
        return cr

    def test_api_functioning(self):
        r = self.fetch("/api/autocomplete/courses?query=C")
        self.assertEqual(json.loads(str(r.body, encoding='utf-8')), {"query": "C", 'suggestions': ['CS 4641']})
