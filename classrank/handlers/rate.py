from . import BaseHandler
from .forms import RateForm
from classrank.database.tables import Account, Course, Student, Section, Rating
from classrank.database.wrapper import Query, NoResultFound, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from tornado.web import authenticated

"""Handler for sending ratings to the database, given a class and section."""


class RateHandler(BaseHandler):
    @authenticated
    def get(self):
        return self.render("rate.html")

    def post(self):
        """Method that processes information placed into the rate form.

        Results are validated through the 'RateForm' object. If they are
        validated, check the database to see if the given course and section
        exist. If so, put it in. Else, fail.

        :returns: redirect to '/rate' regardless of success or failure
        """
        form = RateForm(self.request.arguments)

        if form.validate():
            try:
                # store argument data
                name = self.get_argument('name')
                section = self.get_argument('section')
                semester = self.get_argument('semester')
                rating = self.get_argument('rating')
                cur_user = self.__decoded_username()

                with Query(self.db) as q:
                    # get queries for all concerned tables
                    course_q = q.query(Course)
                    section_q = q.query(Section)
                    account_q = q.query(Account)

                    # get needed course, section, and account info from db
                    # calling 'one()' verifies that one match exists
                    course = course_q.filter_by(abbreviation=name).one()

                    section = section_q.filter_by(course_id=course.uid,
                                                  name=section,
                                                  semester=semester).one()

                    account = account_q.filter_by(username=cur_user).one()

                    # generate rating object/row
                    rating = self.db.rating(student_id=account.student.uid,
                                            section_id=section.uid,
                                            rating=rating,
                                            section=section,
                                            student=account.student)
                    # add rating to db
                    q.add(rating)

                    q.query(Rating).filter_by(section=section).one()
                    return self.redirect("/rate")
            except Exception as e:
                return self.redirect("/rate")
        else:
            return self.redirect("/rate")

    def __decoded_username(self):
        """Decodes username from 'get_current_user()'.

        get_current_user method returns a byte array with wrapped double
        quotes inside. For example, the username 'mitchell' would appear as:
                b'"mitchell"'.
        We need to decode the bytes, and strip the quotes off.

        :returns: quote-less string version of get_current_user
        """
        return bytes.decode(self.get_current_user())[1:-1]
