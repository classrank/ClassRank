from . import BaseApiHandler
from classrank.database.wrapper import Query
from sqlalchemy import distinct


class CourseAutocomplete(BaseApiHandler):
    def get(self):
        course = self.request.arguments['query'][0] or ""
        s, n = course.decode('utf-8').partition(" ")[::2]
        with Query(self.db) as q:
            courses = q.query(self.db.course.subject, self.db.course.number).filter(self.db.course.number.like(n+"%"), self.db.course.subject.like(s+"%")).all()
        return self.write({"suggestions": sorted([course[0]+" "+course[1] for course in courses]), "query": course.decode('utf-8')})


class ProfessorGetCourses(BaseApiHandler):
    def get(self):
        professorUsername = self.request.arguments['username']

        with Query(self.db) as q:
            try:
                professor_account_uid = q.query(self.db.account).filter_by(username == professorUsername).one()
                professor = q.query(self.db.faculty).filter_by(uid == professor_account_uid).one()
            except:
                return self.write({"error": "professor not found"})

            sections = q.query(self.db.section).filter_by(professor_id == professor.uid)

            returnVal = []

            for section in sections:
                thisSection = {}
                thisSection["year"] = section.year
                thisSection["semester"] = section.semester
                thisSection["section"] = section.name

                course = q.query(self.db.course).filter_by(uid == section.course_id).one()

                thisSection["name"] = course.subject + " " + course.number

                returnVal.append(thisSection)

            return self.write(returnVal)
