from . import BaseHandler

class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render("register.html")

class LoginHandler(BaseHandler):
    def get(self):
        return self.render("login.html")