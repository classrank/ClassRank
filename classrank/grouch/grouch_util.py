import datetime
import json

from classrank.database.wrapper import Query


"""add_to_database.py: adds courses from Grouch to the ClassRank DB."""


def add_to_database(grouch_output, db):
    """
    Add courses from Grouch's output to a db.

    Keyword arguments:
    grouch_output -- the output of Grouch (the scraped info)
    db -- the db to add to
    """

    print("Beginning Grouch parse ({}).".format(datetime.datetime.now()))
    all_courses = parse(grouch_output)
    print("Ending Grouch parse ({}).".format(datetime.datetime.now()))

    print("Beginning database add ({}).".format(datetime.datetime.now()))
    with Query(db) as q:

        school_dict = {"name": "Georgia Institute of Technology",
                       "abbreviation": "gatech"}

        if not _school_in_database(school_dict, db, q):
            q.add(db.school(**school_dict))

        school_id = q.query(db.school).filter_by(**school_dict).one().uid

        for course, sections in all_courses:
            course_dict = {"school_id": school_id,
                           "name": course['name'],
                           "description": course['fullname'],
                           "number": course['number'],
                           "subject": course['school']}

            if not _course_in_database(course_dict, db, q):
                q.add(db.course(**course_dict))

            course_id = q.query(db.course).filter_by(**course_dict).one().uid

            for section in sections:
                section_dict = {"course_id": course_id,
                                "semester": course['semester'],
                                "year": course['year'],
                                "name": section['section_id'],
                                "crn": section['crn']}

                q.add(db.section(**section_dict))

    print("Ending database add ({}).".format(datetime.datetime.now()))


def parse(to_read):
    """Parse Grouch output (JSON) to dictionaries, with some additions.

    Keyword arguments:
    to_read -- the file of Grouch output (one JSON document per line)

    Return a list of tuples of (course, sections_of_course).
    """

    # A mapping of semester number to string name
    semester_map = {'2': 'Spring',
                    '5': 'Summer',
                    '8': 'Fall'}

    all_courses = []

    with open(to_read, 'r') as f:
        for line in f:
            course = json.loads(line)

            # Extract the semester and year for easier use later
            semester_token = course['semester']  # of the form yyyymm
            year = semester_token[0:4]
            month = semester_token[5:6]
            semester = semester_map[month]

            course['year'] = year
            course['semester'] = semester

            sections = []

            if 'sections' in course:  # If the course has sections
                sections = course['sections']

            all_courses.append((course, sections))

    return all_courses


def _school_in_database(school_dict, db, q):
    """Check if a school is in the database.

    Keyword arguments:
    school_dict -- a dictionary specifying the school to check
    db -- the db to search in
    q -- the Query object used to query the database

    Returns True if there are instances of school in database, False otherwise
    """
    return len(q.query(db.school).filter_by(**school_dict).all()) != 0


def _course_in_database(course_dict, db, q):
    """Check if a course is in the database.

    Keyword arguments:
    course_dict -- a dictionary specifying the course to check
    db -- the db to search in
    q -- the Query object used to query the database

    Returns True if there are instances of course in database, False otherwise
    """
    return len(q.query(db.course).filter_by(**course_dict).all()) != 0
