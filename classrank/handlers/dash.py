from tornado.web import authenticated

from . import BaseHandler

class DashHandler(BaseHandler):
    @authenticated
    def get(self):
        return self.render("dash.html")
