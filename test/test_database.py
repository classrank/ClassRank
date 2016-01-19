import unittest

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from classrank.database.tables import School, Account, Student, Faculty, Base, Course, Section, Rating


class TestTables(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://')  # create in memory db
        self.metadata = Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def build_relationship(self):
        tech = School(name="Georgia Institute of Technology", abbreviation="gatech")
        user = Account(username="Josh", email_address="me@cr.com",
                       password_hash="a", password_salt="b")
        student = Student(school=tech, account=user)
        professor_account = Account(username="Jay", email_address="me@gatech.edu",
                                    password_hash="c", password_salt="d")
        professor = Faculty(school=tech, account=professor_account)
        course = Course(school=tech, abbreviation="CS1331", name="Introduction to Java")
        section = Section(professor=professor, semester=2, year=2015,
                          course=course)
        rating = Rating(rating=3, section=section, student=student)
        del self
        return locals()

    def test_account_basic(self):
        # you can add an account
        self.session.add(Account(username="bob", email_address="m@test.com",
                                 password_hash="secret", password_salt="table"))
        self.session.commit()
        # and it persists
        self.assertEqual("bob", self.session.query(Account).all()[0].username)
        self.assertEqual("m@test.com", self.session.query(Account).all()[0].email_address)
        self.assertEqual("secret", self.session.query(Account).all()[0].password_hash)
        self.assertEqual("table", self.session.query(Account).all()[0].password_salt)

    def test_account_nulls(self):
        # prevents you from adding broken things to the database, or in other words that
        # the nullable=True rules are all correct
        self.session.add(Account())
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", email_address="addr",
                                 password_hash="pw"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", email_address="addr",
                                 password_salt="salt"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", password_hash="pw",
                                 password_salt="salt"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(email_address="addr", password_salt="salt",
                                 password_hash="pw"))
        self.assertRaises(IntegrityError, self.session.commit)

    def test_school_nulls(self):
        self.session.add(School())
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(School(name="testschool"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(School(abbreviation="testabbr"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()

    def test_course_nulls(self):
        self.session.add(Course())
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Course(school_id=None, name="example"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()

    def test_relationships(self):
        # makes sure that the basic relationship mappings outlined work as intended
        # this does not test any strange edge cases
        vs = self.build_relationship()
        self.session.add_all(x for x in vs.values())
        self.session.commit()
