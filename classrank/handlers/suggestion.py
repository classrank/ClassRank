from tornado.web import authenticated

from classrank.database.wrapper import Query
from . import BaseHandler
from classrank.filters.collabfilter import CollaborativeFilter



class SuggestionHandler(BaseHandler):
    @authenticated
    def get(self):
        page_data = {"error": False, "data":{}}
        user = self.decoded_username()
        data = dict()
        try:
            filters = self.add_filters()
            with Query(self.db) as q:
                student = q.query(self.db.account).filter_by(username=user).one().student
                courses = set(c[0] for c in q.query(self.db.course.name).all()) - set([c.name for c in student.courses])
                student_id = student.uid
            ratings = filters['rating'].getRecommendation({student_id: courses})[student_id]
            page_data['data']['rating'] = sorted([(k, v) for k, v in ratings.items()], key=lambda x: x[1] or 0)[::-1]
            self.render('suggestion.html', **page_data)
        except Exception as e:
            print(e)
            page_data['error'] = True
            self.render("suggestion.html", **page_data)



    def add_filters(self):
        # attrs = set(x for x in dir(self.db.rating) if not x.startswith("_"))
        # attrs -= set(["metadata", "section_id", "student", "section", "student_id"])
        # return {attr: CollaborativeFilter(db=self.db, metric=attr) for attr in attrs}
        with Query(self.db)as q:
            num = max(1, int(q.query(self.db.student).count() / 5))
        return {'rating': CollaborativeFilter(db=self.db, metric='rating', numRecommendations=num)}