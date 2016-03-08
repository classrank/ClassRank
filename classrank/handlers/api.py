from . import BaseApiHandler
from classrank.database.wrapper import Query
from sqlalchemy import distinct


class CourseAutocomplete(BaseApiHandler):
    def get(self):
        course = self.request.arguments['query'][0] or ""
        s, n = course.decode('utf-8').partition(" ")[::2]
        print(s)
        print(n)
        with Query(self.db) as q:
            courses = q.query(self.db.course.subject, self.db.course.number).filter(self.db.course.number.like(n+"%"), self.db.course.subject.like(s+"%")).all()
        return self.write({"suggestions": sorted([course[0]+" "+course[1] for course in courses]), "query": course.decode('utf-8')})