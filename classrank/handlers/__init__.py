import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db
