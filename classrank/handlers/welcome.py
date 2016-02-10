from tornado.web import authenticated

from . import BaseHandler


class WelcomeHandler(BaseHandler):
    @authenticated
    def get(self):
        return self.write("You're allowed here!")
