import unittest
import shutil
import os

from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from classrank.database.tables import School, Account, Student, Faculty, Base, Course, Section, Rating
from classrank.database.wrapper import Database, Query


class TestTables(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(os.environ.get('CONNECTION', 'sqlite://'))  # create in memory db
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def build_relationship(self):
        tech = School(name="Georgia Institute of Technology", abbreviation="gatech")
        user = Account(username="Josh", email_address="me@cr.com",
                       password_hash=b"a", password_salt=b"b")
        student = Student(school=tech, account=user)
        professor_account = Account(username="Jay", email_address="me@gatech.edu",
                                    password_hash=b"c", password_salt=b"d")
        professor = Faculty(school=tech, account=professor_account)
        course = Course(school=tech, number="1331", subject="CS", name="Introduction to Java")
        section = Section(professor=professor, semester=2, year=2015,
                          course=course)
        rating = Rating(rating=3, section=section, student=student)
        del self
        return locals()

    def test_account_basic(self):
        # you can add an account
        self.session.add(Account(username="bob", email_address="m@test.com",
                                 password_hash=b"secret", password_salt=b"table"))
        self.session.commit()
        # and it persists
        self.assertEqual("bob", self.session.query(Account).all()[0].username)
        self.assertEqual("m@test.com", self.session.query(Account).all()[0].email_address)
        self.assertEqual(b"secret", self.session.query(Account).all()[0].pw_hash)
        self.assertEqual(b"table", self.session.query(Account).all()[0].pw_salt)
        self.session.close()

    def test_account_nulls(self):
        # prevents you from adding broken things to the database, or in other words that
        # the nullable=True rules are all correct
        self.session.add(Account())
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", email_address="addr",
                                 password_hash=b"pw"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", email_address="addr",
                                 password_salt=b"salt"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(username="name", password_hash=b"pw",
                                 password_salt=b"salt"))
        self.assertRaises(IntegrityError, self.session.commit)
        self.session.rollback()
        self.session.add(Account(email_address="addr", password_salt=b"salt",
                                 password_hash=b"pw"))
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
        self.session.close()

    def tearDown(self):
        self.metadata.bind = self.engine
        self.metadata.drop_all()


class TestWrapper(unittest.TestCase):
    def setUp(self):
        self.db = Database(engine=os.environ.get("CONNECTION", "sqlite://"))

    def test_query_throws(self):
        with self.assertRaises(IntegrityError):
            with Query(self.db) as q:
                q.add(Account())

    def test_query_working(self):
        with Query(self.db) as q:
            q.add(Account(username="a", email_address="b", password_hash=b"c",
                          password_salt=b"d"))

        with Query(self.db) as q:
            acct = q.query(Account).one()
            self.assertEqual("a", acct.username)

    def test_nested_queries(self):
        with Query(self.db) as outer:
            with Query(self.db) as inner:
                inner.add(Account(username="a", email_address="b", password_hash=b"c",
                          password_salt=b"d"))
            acct = outer.query(Account).one()
            self.assertEqual("a", acct.username)

    def test_cleanup(self):
        with self.assertRaises(TypeError):
            with Query(self.db) as q:
                with patch.object(q.session, 'rollback', return_value=5) as mock_rollback:
                    raise TypeError
                self.assertEqual(mock_rollback.called, True)

    def tearDown(self):
        self.db.metadata.drop_all()
