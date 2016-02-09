import os

from tornado.testing import AsyncHTTPTestCase

from classrank.app import ClassRankApp
from classrank.routing import routes

test_cookie_secret = "secret_cookie"


class TestApplication(AsyncHTTPTestCase):
    def get_app(self):
        self.settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "../classrank/static"),
            "template_path": os.path.join(os.path.dirname(__file__),
                                          "../classrank/templates"),
            "pages": ["Page", "Other Page"]
        }
        return ClassRankApp(None, routes, **self.settings)

    def test_splash(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertIn("ClassRank".encode('utf-8'), response.body)

    def test_login(self):
        response = self.fetch("/login")
        self.assertEqual(response.code, 200)

    def test_register(self):
        response = self.fetch("/register")
        self.assertEqual(response.code, 200)

    def setUp(self):
        import tornado.netutil
        import socket
        
        socks = tornado.netutil.bind_sockets(None, 'localhost', family=socket.AF_INET, reuse_port=False)
        print(socks)
        print(dir(socks[0]))
        self.assertEqual(1, 0)
