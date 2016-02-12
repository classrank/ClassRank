import unittest
from unittest.mock import Mock, MagicMock, patch

from tornado.web import RequestHandler

from classrank.handlers import BaseHandler

test_cookie_secret = "secret_cookie"

class TestBaseHandler(unittest.TestCase):
    def setUp(self):
        self.app = MagicMock()
        self.app.db = "database"
        self.app.settings = {"pages": None}

    def test_base_handler(self):
        handler = BaseHandler(self.app, Mock())
        self.assertEqual(handler.db, "database")
        self.assertEqual(handler.pages, None)

        template = "file.html"
        with patch.object(RequestHandler, "render", return_value="a template") as r:
            handler.render(template)
            args, kwargs = r.call_args
        self.assertTupleEqual((args, kwargs), (
            ("file.html",), {"pages": None}))
