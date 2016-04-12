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
        # TODO: populate dropdown lists with courses taught by prof
        courses = []
        course1 = {}
        course2 = {}
        course3 = {}
        course4 = {}
        course5 = {}
        course6 = {}
        course7 = {}
        course8 = {}
        course9 = {}
        course10 = {}

        course1["year"] = 2013
        course1["semester"] = "fall"
        course1["name"] = "CS 1100"
        course1["section"] = "A"

        course2["year"] = 2013
        course2["semester"] = "fall"
        course2["name"] = "CS 1332"
        course2["section"] = "N"

        course3["year"] = 2013
        course3["semester"] = "fall"
        course3["name"] = "CS 1332"
        course3["section"] = "M"

        course4["year"] = 2014
        course4["semester"] = "spring"
        course4["name"] = "CS 1100"
        course4["section"] = "A"

        course5["year"] = 2014
        course5["semester"] = "spring"
        course5["name"] = "CS 1100"
        course5["section"] = "B"

        course6["year"] = 2014
        course6["semester"] = "spring"
        course6["name"] = "CS 4400"
        course6["section"] = "X"

        course7["year"] = 2014
        course7["semester"] = "summer"
        course7["name"] = "CS 4400"
        course7["section"] = "L"

        course8["year"] = 2014
        course8["semester"] = "fall"
        course8["name"] = "CS 2110"
        course8["section"] = "A"

        course9["year"] = 2014
        course9["semester"] = "fall"
        course9["name"] = "CS 2110"
        course9["section"] = "B"

        course10["year"] = 2015
        course10["semester"] = "fall"
        course10["name"] = "CS 3451"
        course10["section"] = "H"

        courses.append(course1)
        courses.append(course2)
        courses.append(course3)
        courses.append(course4)
        courses.append(course5)
        courses.append(course6)
        courses.append(course7)
        courses.append(course8)
        courses.append(course9)
        courses.append(course10)

        sorted(courses, key=course_section)
        sorted(courses, key=course_name)
        sorted(courses, key=course_semester)
        sorted(courses, key=course_year)

        return self.render("prof_view.html", courses=courses)
    
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