import tornado.ioloop
import tornado.web
import argparse
from classrank.routing import routes
from classrank.app import ClassRankApp
import os
import json


def parser():
    p = argparse.ArgumentParser(description="ClassRank webserver configuration")
    p.add_argument('-p', '--port', default=os.environ.get('port', 8000))
    p.add_argument('-s', '--settings', default=os.environ.get('settings', 'config.json.example'))
    return p


if __name__ == "__main__":
    parser = parser()
    args = parser.parse_args()
    settings = dict()
    try:
        with open(args.settings) as f:
            settings = json.loads(f)
    except FileNotFoundError:
        # no additional settings file so we ignore
        pass

    app = ClassRankApp(None, routes, settings)
    app.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
