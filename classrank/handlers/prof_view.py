from . import BaseHandler
from .forms import SettingsForm
from . import _authenticate as authenticate
from classrank.database.tables import Account, Course, Student, Section, Rating
from classrank.database.wrapper import Query, NoResultFound, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tornado.web import authenticated

"""Handler for changing settings for a user."""

class ProfViewHandler(BaseHandler):
    """Passes an array with the logged in professors courses to the renderer.
    This dictionary gets filtered and displayed via javascript that executes when
    the user selects items in the dropdown menus.

    Each course is a dictionary, with the keys "year" "semester" "name" and "section"

    The array is sorted chronologically, then by course name, then by section letter"""
    @authenticated
    def get(self):        
        return self.render("prof_view.html", username=str(self.__decoded_username()))
    
    def _get_current_user_email(self):
        current_user = self.__decoded_username()
        
        with Query(self.db) as q:
            user = q.query(self.db.account).filter_by(username=current_user).one()
            return user.email_address


    def __decoded_username(self):
        """Decodes username from 'get_current_user()'.

        get_current_user method returns a byte array with wrapped double
        quotes inside. For example, the username 'mitchell' would appear as:
                b'"mitchell"'.
        We need to decode the bytes, and strip the quotes off.

        :returns: quote-less string version of get_current_user
        """
        return bytes.decode(self.get_current_user())[1:-1]

#custom functions for sorting
def course_year(course):
    return course["year"]

def course_semester(course):
    if course["semester"] == "fall":
        return 1
    elif course["semester"] == "summer":
        return 2
    else:
        return 3

def course_name(course):
    return course["name"]

def course_section(course):
    return course["section"]
