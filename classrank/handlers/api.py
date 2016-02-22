from . import BaseApiHandler
from classrank.database.wrapper import Query


class SchoolApi(BaseApiHandler):
    def get(self, prefix):
        prefix = prefix or ""
        with Query(self.db) as q:
            courses = q.query(self.db.course.abbreviation).filter(self.db.course.abbreviation.like(prefix+"%")).all()
        return self.write({"courses": [course[0] for course in courses]})
