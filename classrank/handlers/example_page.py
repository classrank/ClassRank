from . import BaseHandler

class ExampleHandler(BaseHandler):
    def get(self):
        self.render("base.html")
