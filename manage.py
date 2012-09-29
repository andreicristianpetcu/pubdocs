#!/usr/bin/env python

import os
import flask
from flask.ext.script import Manager
import harvest


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('settings.py', silent=True)
    return app


manager = Manager(create_app)

harvest.register_commands(manager)


if __name__ == '__main__':
    from utils import set_up_logging
    set_up_logging()
    manager.run()
