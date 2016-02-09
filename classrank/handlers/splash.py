from . import BaseHandler

class SplashHandler(BaseHandler):
    def get(self):
        self.render("splash.html")
