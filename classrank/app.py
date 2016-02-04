import tornado.web
import classrank.database.wrapper as db


class ClassRankApp(tornado.web.Application):
    def __init__(self, db_connection: tuple or None, *args, **kwargs):
        """

        :param db_connection: tuple of arguments to the database
        """
        super(ClassRankApp, self).__init__(*args, **kwargs)

        #initialize database
        if db_connection is None:
            self.db = db.Database()
        else:
            self.db = db.Database(*db_connection)
