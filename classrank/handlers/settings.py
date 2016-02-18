from . import BaseHandler
from .forms import SettingsForm
from . import _authenticate as authenticate
from classrank.database.tables import Account, Course, Student, Section, Rating
from classrank.database.wrapper import Query, NoResultFound, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tornado.web import authenticated

"""Handler for changing settings for a user."""

class SettingsHandler(BaseHandler):
    @authenticated
    def get(self):
        current_user = self.__decoded_username()

        with Query(self.db) as q:
            user = q.query(self.db.account).filter_by(username=current_user).one()
            email = user.email_address

        # populate email field with pre-existing email from database
        # update_success is True when the page is reloaded upon a successful update
        return self.render("settings.html", email=email, errors={}, update_success=False)

    def post(self):
        errors = dict()
        success = False
        form = SettingsForm(self.request.arguments)
        current_user = self.__decoded_username()

        if form.validate():
            try:
                current_password = self.get_argument('current_password')
                new_password = self.get_argument('new_password')
                new_password_confirm = self.get_argument('new_password_confirm')
                new_email = self.get_argument('new_email')

                with Query(self.db) as q:
                    # first, ensure that current_password is correct
                    user = q.query(self.db.account).filter_by(username=current_user).one()
                    h = user.password_hash
                    s = user.password_salt

                    if authenticate.hash_pw(current_password, s) == h:
                        # current password is authenticated, information has been validated.
                        # now update database with new info

                        # remember, they can omit new password form-- this leaves password unchanged
                        if len(new_password) > 0:
                            user.password_hash, user.password_salt = authenticate.create_password(new_password)

                        # they can't omit this form, but it autofills to their current email on page
                        # load, so as long as they don't touch it everything is gucci
                        user.email_address = new_email
                        email = new_email #snag it here so we can pass it in in the self.render(...) call

                        success = True
                    else:
                        errors['password'] = ["Incorrect password"]
                        email = user.email_address

            except Exception as e:
                errors['unknown'] = [sys.exc_info()[0]]
        else:
            # Invalid forms-- have to re-query the old email address to prepopulate it
            errors = form.errors

            with Query(self.db) as q:
                user = q.query(self.db.account).filter_by(username=current_user).one()
                email = user.email_address

        return self.render("settings.html", email=email, errors=errors, update_success=success)


    def __decoded_username(self):
        """Decodes username from 'get_current_user()'.

        get_current_user method returns a byte array with wrapped double
        quotes inside. For example, the username 'mitchell' would appear as:
                b'"mitchell"'.
        We need to decode the bytes, and strip the quotes off.

        :returns: quote-less string version of get_current_user
        """
        return bytes.decode(self.get_current_user())[1:-1]