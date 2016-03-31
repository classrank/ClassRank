from itsdangerous import URLSafeTimedSerializer
from classrank.database.wrapper import Query
from . import BaseHandler
import datetime

class ConfirmEmailHandler(BaseHandler):

    def get(self):
        return self.render("confirm.html", errors={})

    def post(self, token):
        errors = dict()
        token = self.get_token_from_url(BaseHandler.request.uri)
        try:
            email = self.confirm_email_token(token)
        except:
            errors['confirm'] = ["Confirmation Invalid"]
        user = Query(self.db).query(self.db.account).filter_by(
                            email_address=email).one()
        if user.confirmed:
            errors['confirm'] = ["Account already confirmed."]
        else:
            user.confirmed = True
            user.confirmed_on = datetime.datetime.now()
            Query(self.db).add(user)
        return self.render("dash.html")

    def get_token_from_url(self, url):
        #this is super shady and i don't like it, pls help
        return url[26:]

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