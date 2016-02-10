import classrank.handlers.auth as auth
import classrank.handlers.splash as splash
import classrank.handlers.welcome as welcome

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/register/?', auth.RegistrationHandler),
    (r'/welcome/?', welcome.WelcomeHandler),
]