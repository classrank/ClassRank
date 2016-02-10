import tornado.escape

from classrank.database.wrapper import Query, NoResultFound, IntegrityError
from . import BaseHandler
from . import _authenticate as authenticate
from .forms import LoginForm, RegistrationForm


class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render("register.html")

    def post(self):
        form = RegistrationForm(self.request.arguments)
        if form.validate():
            h, s = authenticate.create_password(self.get_argument('password'))
            user = self.db.account(username=self.get_argument('username'),
                                   email_address=self.get_argument('email'),
                                   password_hash=h, password_salt=s)
            try:
                with Query(self.db) as q:
                    q.add(user)
                    return self.render('login.html')
            except IntegrityError:
                # TODO: toss an error message up or do this through an api interface
                # instead of directly
                return self.render('register.html')
            except Exception as e:
                raise
        else:
            return self.render('register.html')


class LoginHandler(BaseHandler):
    def get(self):
        return self.render("login.html")

    def post(self):
        form = LoginForm(self.request.arguments)
        if form.validate():
            try:
                with Query(self.db) as q:
                    user = q.query(self.db.account).filter_by(
                        email_address=self.get_argument('email')).one()
                    h = user.password_hash
                    s = user.password_salt

                    if authenticate.hash_pw(self.get_argument('password'), s) == h:
                        self.authorize(user.username)
                        return self.redirect('/welcome')
            except NoResultFound:
                return self.render("login.html")

    def authorize(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")
