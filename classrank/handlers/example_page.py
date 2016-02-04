from . import BaseHandler

class ExampleHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")
        print(self.application.db)