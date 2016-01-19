import sqlalchemy
import sqlalchemy.orm
from classrank.database import tables

class Database:
    def __init__(self, engine="sqlite:///", name="ClassRank.db", folder="temp"):

        self.account = tables.Account
        self.student = tables.Student
        self.rating = tables.Rating
        self.course = tables.Course
        self.section = tables.Section
        self.faculty = tables.Faculty
        self.school = tables.School
        if name == None and folder == None:
            self.engine = sqlalchemy.create_engine(engine)
        else:
            self.engine = sqlalchemy.create_engine(engine + folder + "/" + name)
        self.base = tables.Base
        self.metadata = self.base.metadata
        self.metadata.create_all(self.engine)
        self.Session = sqlalchemy.orm.sessionmaker(bind=self.engine)


class Query:
    """
    The Query class is a wrapper for database actions, all functions that interface with
    the database should do so through the query or database wrappers.
    """
    def __init__(self, db: Database):
        self.db = db

        # lift all tables into the query
        for attr in ["account", "student", "rating", "course", "section", "faculty",
                      "school"]:
            self.__setattr__(attr, self.db.__getattribute__(attr))

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