from classrank.database.wrapper import Query

"""add_to_database.py: adds courses from Grouch to the ClassRank DB."""


def add_to_database(grouch_output, db):
    """
    Add courses from Grouch's output to a db.

    Keyword arguments:
    grouch_output -- the output of Grouch (the scraped info)
    db -- the db to add to
    """

    all_courses = parse(grouch_output)

    with Query(db) as q:

        # Begin by adding GT, if it's not already there
        try:
            q.add(db.school(**{"name": "Georgia Institute of Technology",
                               "abbreviation": "gatech"}))
        except:
            pass  # Already added, we're fine

        # Get the generated school id for backrefs and relationships
        school_id = q.filter(course.abbreviation == "gatech").one()[uid]

        for course, sections in all_courses:
            # Add the course
            q.add(db.course(**{"school_id": school_id,
                               "name": course['name'],
                               "description": course['fullname'],
                               "number": course['number'],
                               "subject": course['school']}))

            # Get the generated course id for backrefs and relationsships
            course_id = q.filter(course.school_id == school_id,
                                 course.name == course['name'],
                                 course.description == course['fullname'],
                                 course.number == course['number'],
                                 course.subject == course['school']).one()[uid]

            # Then, add the corresponding sections
            for section in sections:
                q.add(db.section(**{"course_id": course_id,
                                    "semester": course[semester],
                                    "year": course[year],
                                    "name": section[section_id],
                                    "crn": section[crn]}))


def parse(to_read, lines=None):
    """
    Return a list of tuples of (course, sections_of_course).
    """

    # A mapping of semester number to string name
    semester_map = {'2': 'Spring',
                    '5': 'Summer',
                    '8': 'Fall'}

    all_courses = []

    with open(to_read, 'r') as f:

        if lines is None:
            lines = sum(1 for line in f)

        for _ in range(0, lines):
            line = f.readline()
            course = json.loads(line)

            # Extract the semester and year for easier use later
            semester_token = course[semester]  # of the form yyyymm
            year = semester_token[0:4]
            month = semester_token[5:6]
            semester = semester_map[month]

            course[year] = year
            course[semester] = semester

            if 'sections' in course:  # If the course has sections
                sections = course['sections']

        all_courses.append((course, sections))


def main():
    in_file = sys.argv[1]
    if (len(sys.argv) == 3):
        number_of_lines_to_read = int(sys.argv[2])

    parsed = parse(in_file, number_of_lines_to_read)

if __name__ == '__main__':
    main()
