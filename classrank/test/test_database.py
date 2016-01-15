import unittest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from classrank.database.tables import School, Account, Student, Faculty, Base, Course, Section, Rating
from sqlalchemy import create_engine
from classrank import database


class TestTables(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://')  # create in memory db
        self.metadata = Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

    def test_account(self):
        # you can add an account
        self.session.add(Account(username="bob", email_address="me@test.com",
                                 password_hash="secret", password_salt="table"))
        self.session.commit()
        # and it persists
        self.assertEqual("bob", self.session.query(Account).all()[0].username)