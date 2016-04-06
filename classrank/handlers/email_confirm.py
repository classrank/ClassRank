from itsdangerous import URLSafeTimedSerializer
from classrank.database.wrapper import Query
from . import BaseHandler
import datetime, smtplib

class ConfirmEmailHandler(BaseHandler):

    def get(self, token):
        return self.render("confirm.html", errors={})

    def post(self, token):
        errors = dict()

        """Verify that the email token is valid"""
        try:
            email = self.confirm_email_token(token)
        except:
            errors['confirm'] = ["Confirmation Invalid"]
            return self.render("confirm.html", errors=errors)

        user = Query(self.db).query(self.db.account).filter_by(
                            email_address=email).one()

        """Confirm user isn't confirmed already"""
        if user.confirmed:
            errors['confirm'] = ["Account already confirmed."]
            return self.render("confirm.html", errors=errors)
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            Query(self.db).add(user)
            return self.render("dash.html")

    def generate_confirmation_email_token(self, email):
        token = URLSafeTimedSerializer('cookie-secret')
        return token.dumps(email, salt='security-password-salt')

    def confirm_email_token(self, token, expiration=3600):
        token = URLSafeTimedSerializer('cookie-secret')
        try:
            email = token.loads(token, salt='security-password-salt', max_age=expiration)
        except:
            return False
        return email

    def send_email(self, recipient, template):
        server = smtplib.SMTP('localhost')
        server.sendmail('email_sender', recipient, template)
        server.quit()
