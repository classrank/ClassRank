import tornado.web

class ExampleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")