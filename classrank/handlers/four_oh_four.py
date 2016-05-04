import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler gonna to be used instead of RequestHandler
    """
    def write_error(self, status_code, **kwargs):

        error_info = {
            'error': status_code,
            'unknown_url': self.request.uri
        }

        self.render("error.html", **error_info)


class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    """
    Default handler gonna to be used in case of 404 error
    """
    pass
