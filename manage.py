#!/usr/bin/env python

import os
from path import path
import flask
from flask.ext.script import Manager
import harvest
import search


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py', silent=True)
    app.config['PUBDOCS_FILE_REPO'] = path(os.environ.get('PUBDOCS_FILE_REPO')
                                           or app.instance_path)
    if 'PUBDOCS_ES_URL' in os.environ:
        app.config['PUBDOCS_ES_URL'] = os.environ['PUBDOCS_ES_URL']
    return app


manager = Manager(create_app)

harvest.register_commands(manager)
search.register_commands(manager)


if __name__ == '__main__':
    from utils import set_up_logging
    set_up_logging()
    manager.run()
