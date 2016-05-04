from tornado.web import StaticFileHandler

import classrank.handlers.api as api
import classrank.handlers.auth as auth
import classrank.handlers.dash as dash
import classrank.handlers.info as info
import classrank.handlers.rate as rate
import classrank.handlers.settings as settings
import classrank.handlers.splash as splash
import classrank.handlers.suggestion as suggestion

routes = [
    (r'/', splash.SplashHandler),
    (r'/about', info.AboutHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/logout/?', auth.LogoutHandler),
    (r'/privacy', info.PrivacyHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/rate/?', rate.RateHandler),
    (r'/security', info.SecurityHandler),
    (r'/settings/?', settings.SettingsHandler),
    (r'/dashboard/?', dash.DashHandler),
    (r'/search/?', suggestion.SuggestionHandler),
    (r'/favicon.ico', StaticFileHandler, {'path': 'static/favicon.ico'}),



    # api handlers
    (r'/api/autocomplete/courses/?', api.CourseAutocomplete),

]
