import tornado.web
import tornado.escape
import json

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.db = self.application.db

    def render(self, template_name, **kwargs):
        """
        binds certain global settings so that they are always passed into the template
        """
        if(self.get_current_user()):
            pages = self.application.settings['logged_in_pages']
        else:
            pages = self.application.settings['logged_out_pages']

        kwargs['pages'] = pages
        return super(BaseHandler, self).render(template_name, **kwargs)

    def get_current_user(self):
        return self.get_secure_cookie("user")


class BaseApiHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.application.db

    def write(self, dict):
        super().write(json.dumps(dict, sort_keys=True, indent=4, separators=(',', ': ')))
        self.add_header('Content-Type', 'application/json')
