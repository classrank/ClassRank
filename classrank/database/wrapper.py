import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from classrank.database import tables

IntegrityError = IntegrityError

class Database:
    def __init__(self, engine="sqlite://"):
        """
        engine: a database connections string
        """

        self.account = tables.Account
        self.student = tables.Student
        self.rating = tables.Rating
        self.course = tables.Course
        self.section = tables.Section
        self.faculty = tables.Faculty
        self.school = tables.School
        self.engine = sqlalchemy.create_engine(engine)
        self.base = tables.Base
        self.metadata = self.base.metadata
        self.metadata.create_all(self.engine)
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)

    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)


class Query:
    """
    The Query class is a wrapper for database actions, all functions that interface with
    the database should do so through the query or database wrappers.
    """
    def __init__(self, db: Database):
        self.db = db

    def __enter__(self):
        self.session = self.db.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def add(self, item):
        """
        A lift of the session.add method
        """
        return self.session.add(item)

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)
