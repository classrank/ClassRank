import string

from classrank.database.wrapper import Query


def create_test_database(app):
    with Query(app.db) as q:
        # first a school
        s = app.db.school(**{"name": "Georgia Test University", "abbreviation": "test"})
        q.add(s)

    usernames = ["A", "B", "Casey", "D", "E", "Fortnow", "G", "H", "I", "Josh", "K", "L",
                 "Mitchell", "N", "Omojokun", "P", "Q", "R", "S", "T"]

    courses = ["CS 1301", "CS 1331", "CS 1332", "CS 2110", "CS 4641", "MATH 1552",
               "MATH 3406", "ENGL 1101", "ENGL 1102"]

    students = []
    teachers = []
    classes = []
    sections = []
    with Query(app.db) as q:  # now create some accounts and the users
        for username in usernames:
            a = app.db.account(username=username, email_address=username + "@gmail.com",
                               password_hash=b'hash', password_salt=b'salt')
            q.add(a)
            if len(username) > 1:
                f = app.db.faculty(account=a, school=s)
                teachers.append(f)
                q.add(f)

            if username not in {"Fortnow", "Omojokun"}:
                p = app.db.student(account=a, school=s)
                students.append(p)
                q.add(p)
        print(len(students))

        for course in courses:
            subj, _, num = course.partition(" ")
            cs = app.db.course(name=course, subject=subj, number=num, school=s)
            q.add(cs)
            classes.append(cs)

            if cs.subject == "CS":
                for i in range(classes.index(cs) + 1):
                    char = string.ascii_uppercase[i]
                    sec = app.db.section(course=cs, professor=teachers[i], name=char,
                                         semester="Spring", year=2016)
                    sections.append(sec)
                    q.add(sec)

            elif cs.subject == "MATH":
                sec = app.db.section(course=cs, professor=teachers[4], name="A",
                                     semester="Spring", year=2016)
                sections.append(sec)
                q.add(sec)
            else:
                sec = app.db.section(course=cs, name="A", semester="Spring", year=2016)
                sections.append(sec)
                q.add(sec)
                sec = app.db.section(course=cs, name="B", semester="Spring", year=2016)
                sections.append(sec)
                q.add(sec)

            for sec in cs.sections:
                q.add(app.db.rating(section=sec, student=students[0],
                                    rating=1))  # rates all courses one

            for i in range(1, 6):
                if cs.sections:
                    q.add(app.db.rating(section=cs.sections[0], student=students[i],
                                        rating=i))  # each rates section 0 as n

            if cs.subject == "CS":
                if len(cs.sections) > 1:
                    q.add(app.db.rating(section=cs.sections[1], student=students[7],
                                        rating=3))

            if cs.subject == "ENGL":
                if cs.number == "1101":
                    q.add(app.db.rating(section=cs.sections[0], student=students[8],
                                        rating=1))
                    q.add(app.db.rating(section=cs.sections[0], student=students[10],
                                        rating=5))
                else:
                    q.add(app.db.rating(section=cs.sections[1], student=students[9],
                                        rating=5))
                    q.add(app.db.rating(section=cs.sections[0], student=students[11],
                                        rating=1))

            if cs.subject == "CS" and cs.number == "1301":
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[11], rating=1))
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[12], rating=3))
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[13], rating=5))

            if cs.subject == "CS" and cs.number == "1331":
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[11], rating=1))
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[12], rating=3))
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[13], rating=5))

            if cs.subject == "CS" and cs.number == "1332":
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[11], rating=1))
                q.add(
                    app.db.rating(section=cs.sections[0], student=students[12], rating=3))
