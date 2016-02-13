import argparse
import json
import os

import tornado.ioloop
import tornado.web

import classrank.app as app
from classrank.app import ClassRankApp
from classrank.routing import routes
from classrank.database.wrapper import Query


def parser():
    p = argparse.ArgumentParser(description="ClassRank webserver configuration")
    p.add_argument('-p', '--port', default=os.environ.get('port', 8000))
    p.add_argument('-s', '--settings', default=os.environ.get('settings', 'config.json.example'))
    p.add_argument('-d', '--debug', action='store_true')
    return p


if __name__ == "__main__":
    parser = parser()
    args = parser.parse_args()
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "classrank/static"),
        "template_path": os.path.join(os.path.dirname(__file__), "classrank/templates")
    }
    app.settings['debug'] = args.debug

    try:
        with open(args.settings) as f:
            settings.update(json.loads(f.read()))
    except FileNotFoundError:
        # no additional settings file so we ignore
        pass

    db_config = settings['db_config']
    del settings['db_config']
    cr = ClassRankApp(None, routes, **settings)

    with Query(cr.db) as q:
        for table in db_config:
            for item in db_config[table]:
                q.add(cr.db.__getattribute__(table)(**item))


    cr.listen(args.port)
    tornado.ioloop.IOLoop.current().start()
