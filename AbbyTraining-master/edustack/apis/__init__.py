import flask_login as login
import markdown2
import hashlib
import json
import re
import time

from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful import abort
from flask_restful import reqparse
from flask_login import current_user, login_required
from flask_restful.reqparse import Argument
from flask_restful.utils import cors


api = Blueprint('api', __name__)
# api_res = Api(api)
api_res = Api(api, decorators=[cors.crossdomain(origin='*')])

def addArg(**kwargs):
    def wrapper(cls):
        if not hasattr(cls, "argDict"):
            setattr(cls, "argDict", {})
        for k,args in kwargs.items():
            parser = reqparse.RequestParser()
            for i in args:
                parser.add_argument(i)
            cls.argDict[k] = parser
        return cls
    return wrapper

def abortValueError(name, message=""):
    abort(400, message="Arg <{0}> Error! {1}".format(name, message))

class ApiBase(Resource):
    def getArgs(self, argsKey):
        parser = self.argDict[argsKey]
        return parser.parse_args()
    def abortIfArgsEmpty(self, args, keys):
        for k in keys:
            if args[k.name] == '':
                abort(400, message={k.name: 'Can not be empty!'})

ArgEmail = Argument('email', required=True, case_sensitive=False, trim=True,
                    help='Invalid email')
ArgPassword = Argument('password', required=True, help='Invalid password')
ArgRemember = Argument('remember', default='false', case_sensitive=False)
ArgPage = Argument('page', default=1, type=int, help='Invalid page')
ArgFormat = Argument('format', default='')

__all__ = ["auth", "user", "blog", "course"]
from edustack.apis import *