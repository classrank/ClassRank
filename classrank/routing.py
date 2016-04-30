import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.rate as rate
import classrank.handlers.prof_view as prof_view
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
    (r'/prof_view/?', prof_view.ProfViewHandler),



    # api handlers
    (r'/api/autocomplete/courses/?', api.CourseAutocomplete),
    (r'/api/professor/courses/?', api.ProfessorGetCourses),
]
