from itsdangerous import URLSafeTimedSerializer
from classrank.database.wrapper import Query
from . import BaseHandler

class ConfirmEmailHandler(BaseHandler):

	def generate_confirmation_email_token(self, email):
		token = URLSafeTimedSerializer('cookie-secret')
		return token.dumps(email, salt='security-password-salt')

	def confirm_email_token(self, token, expiration=3600):
		token = URLSafeTimedSerializer('secret-key')
		try:
			email = token.loads(token, salt='security-password-salt', max_age=expiration)
		except:
			return False
		return email

	def confirm_email(self,token):
		try:
			email = self.confirm_email_token(token)
		except:
			errors['']
		user = Query(self.db).query(self.db.account).filter_by(
	                        email_address=email).one()
		if user.confirmed:
