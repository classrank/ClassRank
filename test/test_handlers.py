import unittest
from unittest.mock import Mock, MagicMock, patch

from tornado.web import RequestHandler

from classrank.handlers import BaseHandler

test_cookie_secret = "secret_cookie"

class TestBaseHandler(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.app.db = "database"
        self.app.settings = {"logged_in_pages": None, "logged_out_pages": None, "cookie_secret": test_cookie_secret}

    def test_base_handler(self):
        handler = BaseHandler(self.app, Mock())
        self.assertEqual(handler.db, "database")

        template = "file.html"
        with patch.object(RequestHandler, "render", return_value="a template") as r:
            with patch.object(BaseHandler, 'get_current_user', return_value=None) as g:
                handler.render(template)
                args, kwargs = r.call_args
            self.assertTupleEqual((args, kwargs), (("file.html",), {"pages": None}))

