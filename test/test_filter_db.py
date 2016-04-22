import unittest
from unittest.mock import Mock, MagicMock, patch
from classrank.filters.collabfilter import CollaborativeFilter
import numpy as np
import os
from classrank.database.wrapper import Database, Query

class TestDatabaseFilter(unittest.TestCase):
    def setUp(self):
        self.conn = Database(engine=os.environ.get("CONNECTION", "sqlite:///:memory:"))
        school = self.conn.school(name="Georgia Tech", abbreviation="gatech")
        course = self.conn.course(school=school, name="Intro Java", number="1331", subject="CS")
        course2 = self.conn.course(school=school, name="Stuff", number="1332", subject="CS")
        section1 = self.conn.section(course=course, semester="fall", year=2016, name="A1")
        section2 = self.conn.section(course=course, semester="fall", year=2016, name="A2")
        self.section3 = self.conn.section(course=course2, semester="spring",year=2015, name="A")
        account = self.conn.account(username="test", email_address="test@test.com", password_hash=b"t", password_salt=b"t")
        student = self.conn.student(account=account, school=school)
        account2 = self.conn.account(username="test2", email_address="test2@test.com", password_hash=b"t", password_salt=b"t")
        self.student2 = self.conn.student(account=account2, school=school)
        with Query(self.conn) as q:
            q.add(school)
            q.add(course)
            q.add(section1)
            q.add(section2)
            q.add(course2)
            q.add(self.section3)
            q.add(account)
            q.add(student)
            q.add(self.student2)
            q.add(self.conn.rating(student=student, section=section1, rating=5))
            q.add(self.conn.rating(student=self.student2, section=section2, rating=3))
    def test_filter_query(self):
        with self.assertRaises(ValueError):
            cf = CollaborativeFilter(db=self.conn)
        with Query(self.conn) as q:
            q.add(self.conn.rating(student=self.student2, section=self.section3, rating=4))
        cf = CollaborativeFilter(db=self.conn)
        self.assertIsInstance(cf.getData(), type([]))
