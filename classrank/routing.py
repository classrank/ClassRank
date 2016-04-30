import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.rate as rate
import classrank.handlers.dash as dash
import classrank.handlers.email_confirm as email_confirm

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/logout/?', auth.LogoutHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/rate/?', rate.RateHandler),
    (r'/dashboard/?', dash.DashHandler),
    (r'/confirm/<token>/?', email_confirm.ConfirmEmailHandler)
]
