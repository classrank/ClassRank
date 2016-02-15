import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.welcome as welcome
import classrank.handlers.rate as rate

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/logout/?', auth.LogoutHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/welcome/?', welcome.WelcomeHandler),
    (r'/rate/?', rate.RateHandler)
]
