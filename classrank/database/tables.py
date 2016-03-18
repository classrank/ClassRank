from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()  # single base class instance for joins

"""
7 tables: Account, Student, Faculty, School, Course, Section, Rating

Account joins 1-1 to Student and Faculty
Student joins 1-* to Section
Faculty joins 1-* to Section
School joins 1-* to Student, Faculty, and Course
Section joins *-* to Student via Rating
Course joins 1-* to Section
"""


class Account(Base):
    __tablename__ = "account"

    uid = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    email_address = Column(String(128), nullable=False, unique=True)
    password_hash = Column(LargeBinary(128), nullable=False)
    password_salt = Column(LargeBinary(16), nullable=False)
    confirmed = Column(Boolean, nullable=False)

    student = relationship("Student", backref="account", uselist=False)
    faculty = relationship("Faculty", backref="account", uselist=False)

    @property
    def pw_hash(self):
        h = None
        try:
            h = self.password_hash.tobytes()
        except AttributeError:
            h = self.password_hash
        return h

    @property
    def pw_salt(self):
        s = None
        try:
            s = self.password_salt.tobytes()
        except AttributeError:
            s = self.password_salt
        return s

class Student(Base):
    __tablename__ = "student"
    uid = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("school.uid"), nullable=False)
    user_id = Column(Integer, ForeignKey("account.uid"), nullable=False)
    sections = relationship('Section', secondary='rating', backref='student')


class Faculty(Base):
    __tablename__ = "faculty"
    uid = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("school.uid"), nullable=False)
    user_id = Column(Integer, ForeignKey("account.uid"), nullable=True)
    sections = relationship("Section", backref="professor")


class School(Base):
    __tablename__ = "school"
    uid = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    abbreviation = Column(String(16), nullable=False, unique=True)
    students = relationship("Student", backref="school")
    faculty = relationship("Faculty", backref="school")
    courses = relationship("Course", backref="school")


class Course(Base):
    __tablename__ = "course"
    uid = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey("school.uid"), nullable=False)
    name = Column(String(64), nullable=False)
    description = Column(String(2000), nullable=True)
    number = Column(String(4), nullable=False)
    subject = Column(String(4), nullable=False)
    sections = relationship("Section", backref="course")


class Section(Base):
    __tablename__ = "section"
    uid = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey("faculty.uid"))
    course_id = Column(Integer, ForeignKey('course.uid'), nullable=False)
    semester = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    name = Column(String(16))
    crn = Column(Integer)


class Rating(Base):
    __tablename__ = "rating"
    student_id = Column(Integer, ForeignKey('student.uid'), primary_key=True)
    section_id = Column(Integer, ForeignKey('section.uid'), primary_key=True)
    rating = Column(Integer, nullable=True)
    section = relationship('Section', backref='ratings')
    student = relationship('Student', backref='ratings')
