import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.rate as rate
import classrank.handlers.dash as dash
import classrank.handlers.settings as settings
import classrank.handlers.api as api

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/logout/?', auth.LogoutHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/rate/?', rate.RateHandler),
    (r'/settings/?', settings.SettingsHandler),
    (r'/dashboard/?', dash.DashHandler),



    # api handlers
    (r'/api/course_name/([\w-]+)?/?', api.SchoolApi)
]
