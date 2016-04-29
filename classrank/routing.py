import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.rate as rate
import classrank.handlers.dash as dash
import classrank.handlers.settings as settings
import classrank.handlers.api as api
import classrank.handlers.suggestion as suggestion

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/logout/?', auth.LogoutHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/rate/?', rate.RateHandler),
    (r'/settings/?', settings.SettingsHandler),
    (r'/dashboard/?', dash.DashHandler),
    (r'/schedule/?', suggestion.SuggestionHandler),



    # api handlers
    (r'/api/autocomplete/courses/?', api.CourseAutocomplete),

]
