import classrank.handlers.splash as splash
import classrank.handlers.auth as auth

routes = [
    (r'/', splash.SplashHandler),
    (r'/login/?', auth.LoginHandler),
    (r'/register/?', auth.RegistrationHandler),
]