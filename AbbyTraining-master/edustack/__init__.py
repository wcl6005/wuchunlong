'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import datetime
import flask_login
import jinja2Filters
import os
import time

from flask import Flask
from flask_babel import Babel
from inspect import getmembers
from inspect import isfunction
from urlConverter import ConverterDict


def createApp():
    try:
        app = Flask(__name__, instance_relative_config=True)
    except IOError:
        app = Flask(__name__)
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    try:
        app.config.from_envvar('APP_CONFIG_FILE')
    except RuntimeError:
        pass

    return app

def configJinjaFilters(app):
    customFilters = {name: function
                     for name, function in getmembers(jinja2Filters)
                     if isfunction(function)}
    app.jinja_env.filters.update(customFilters)

def configUrlConverter(app):
    for name, converter in ConverterDict.items():
        app.url_map.converters[name] = converter

def configBabel(app):
    Babel(app)

def configLogin(app):
    from edustack.models import db
    from edustack.models.user import User
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

def configBlueprint(app):
    from edustack.views.home import home
    from edustack.views.blog import blog
    from edustack.views.course import course
    from edustack.apis import api
    from edustack.views.manage import manage

    app.register_blueprint(home, url_prefix="")
    app.register_blueprint(home, url_prefix="/home")
    app.register_blueprint(blog, url_prefix="/blog")
    app.register_blueprint(course, url_prefix="/course")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(manage, url_prefix="/manage")

wsgiApp = createApp()
configJinjaFilters(wsgiApp)
configUrlConverter(wsgiApp)
configBabel(wsgiApp)
configLogin(wsgiApp)
configBlueprint(wsgiApp)