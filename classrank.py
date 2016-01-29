import tornado.ioloop
import tornado.web
import argparse
from classrank.routing import routes


def parser():
    p = argparse.ArgumentParser(description="ClassRank webserver configuration")
    p.add_argument('-p', '--port', default=8000)
    return p


if __name__ == "__main__":
    parser = parser()
    args = parser.parse_args()
    app = tornado.web.Application(routes)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
