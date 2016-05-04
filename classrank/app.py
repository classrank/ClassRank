import tornado.web

from classrank.handlers import four_oh_four
import classrank.database.wrapper as db
import classrank.grouch.grouch_util as grouch

class ClassRankApp(tornado.web.Application):
    def __init__(self, db_connection: str or None, *args, **kwargs):
        """

        :param db_connection: tuple of arguments to the database
        """
        super(ClassRankApp, self).__init__(*args, **kwargs)

        # Handle 404s and unknown pages
        self.settings['default_handler_class'] = four_oh_four.ErrorHandler
        self.settings['default_handler_args'] = dict(status_code=404)

        #initialize database
        if db_connection is None:
            self.db = db.Database()
        else:
            self.db = db.Database(db_connection)


        grouch.add_to_database(self.settings['grouch_results'], self.db)
