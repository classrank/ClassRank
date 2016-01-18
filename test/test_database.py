import unittest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from classrank.database.tables import School, Account, Student, Faculty, Base, Course, Section, Rating
from sqlalchemy import create_engine


class TestTables(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://')  # create in memory db
        self.metadata = Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

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

