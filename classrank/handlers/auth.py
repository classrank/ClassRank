import tornado.escape
from tornado.web import authenticated
from tornado.httputil import url_concat

from classrank.database.wrapper import Query, NoResultFound, IntegrityError
from . import BaseHandler
from . import _authenticate as authenticate
from .forms import LoginForm, RegistrationForm
from .email_confirm import ConfirmEmailHandler


class RegistrationHandler(BaseHandler):
    def get(self):
        return self.render("register.html", errors={})

    def post(self):
        errors = dict()
        form = RegistrationForm(self.request.arguments)
        if form.validate():
            h, s = authenticate.create_password(self.get_argument('password'))
            user = self.db.account(username=self.get_argument('username'),
                                   email_address=self.get_argument('email'),
                                   password_hash=h, password_salt=s, confirmed=False, confirmed_on=None)
            try:
                with Query(self.db) as q:
                    q.add(user)
                    print("yes")
                    # q.add(self.db.student(account=user, school=q.query(self.db.school).
                    #                       filter_by(abbreviation=self.get_argument('school')).one()))
            except IntegrityError:
                errors['username'] = ["A user with that username or email address already exists, or invalid school"]
            except Exception:
                raise
            else:
                #on success
                confirm_email = ConfirmEmailHandler()
                confirm_token = confirm_email.generate_confirmation_email_token(self.get_argument('email'))
                confirm_url = url_concat("http://classrank.com/confirm/", confirm_token)
                html = self.render('email.html', confirm_url=confirm_url)
                confirm_email.send_email(self.get_argument('email'), html)
                return self.redirect('/login')
        else:
            errors = form.errors
        return self.render('register.html', errors=errors)


class LoginHandler(BaseHandler):
    def get(self):
        return self.render("login.html", errors={})

    def post(self):
        errors = dict()
        form = LoginForm(self.request.arguments)
        if form.validate():
            try:
                with Query(self.db) as q:
                    user = q.query(self.db.account).filter_by(
                        email_address=self.get_argument('email')).one()
                    h = user.pw_hash
                    s = user.pw_salt

                    if authenticate.hash_pw(self.get_argument('password'), s) == h:
                        self.authorize(user.username)
                        return self.redirect('/dashboard')
                    else:
                        errors['password'] = ["Incorrect password"]
            except NoResultFound:
                errors['email'] = ["No user exists with that email address"]
        else:
            errors = form.errors
        return self.render("login.html", errors=errors)


    def authorize(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class LogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.clear_cookie("user")
        return self.redirect("/")

    @authenticated
    def post(self):
        self.clear_cookie("user")
        return self.redirect("/")
