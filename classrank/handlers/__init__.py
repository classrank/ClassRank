import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db
        self.pages = self.application.settings['pages']

    def render(self, template_name, **kwargs):
        """
        binds certain global settings so that they are always passed into the template
        """
        kwargs['pages'] = self.pages
        return super(BaseHandler, self).render(template_name, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")
