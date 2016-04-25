import tornado.web

import classrank.database.wrapper as db
import classrank.filters.datawrapper as wrapper

class ClassRankApp(tornado.web.Application):
    def __init__(self, db_connection: str or None, *args, **kwargs):
        """

        :param db_connection: tuple of arguments to the database
        """
        super(ClassRankApp, self).__init__(*args, **kwargs)

        #initialize database
        if db_connection is None:
            self.db = db.Database()
        else:
            self.db = db.Database(db_connection)

        attrs = set(x for x in dir(self.db.rating) if not x.startswith("_"))
        attrs -= set(["metadata", "section_id", "student", "section", "student_id"])

        self.filters = {attr: wrapper.DataWrapper(db=self.db, metric=attr) for attr in attrs}
        # TODO: add support for multiple schools

settings = {'debug': False,}
