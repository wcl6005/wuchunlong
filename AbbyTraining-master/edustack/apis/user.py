'''
Created on 2016-04-12

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
import re

from flask_login import login_user, login_required, current_user
from flask_restful import abort

from edustack.apis import addArg, abortValueError, api_res, ApiBase, ArgPage,\
    ArgFormat, ArgEmail, ArgPassword
from edustack.utils import tryParse
from edustack.models import toDict, get_items_by_page, db
from edustack.models.user import User, LocalAuth
from flask_restful.reqparse import Argument


ArgUserName = Argument('name', required=True, trim=True, help='Invalid name')

@addArg(getUser=[ArgPage])
@addArg(postUser=[ArgUserName, ArgEmail, ArgPassword])
class API_Users(ApiBase):
    @login_required
    def get(self):
        if not current_user.admin:
            abort(403, message="Admin only")
        args = self.getArgs("getUser")

        users, page = get_items_by_page(args['page'], User)
        return dict(users=[toDict(i) for i in users], page=page.toDict())

    def post(self):
        args = self.getArgs('postUser')
        name = args['name']
        email = args['email']
        password = args['password']

        valRegexDict = User._regexMapDict
        valDict = {'email': args['email'], 'password':args['password']}
        valList = [i for i in valDict if i in valRegexDict]
        for i in valList:
            reCmp = re.compile(valRegexDict[i])
            if not reCmp.match(valDict[i]):
                abortValueError(i)

        user = User.query.filter_by(email=email).first()
        if user:
            abort(400, message="Email is already in use.")

        user = User(name=name, email=email,
                    image='http://www.gravatar.com/avatar/{0}?d=mm&s=120'
                    .format(hashlib.md5(email).hexdigest()))
        db.session.add(user)
        localAuth = LocalAuth(user_id=user.id, password=password)
        db.session.add(localAuth)
        db.session.commit()
        login_user(user)
        
        user = User.query.filter_by(id=user.id).first()
        return toDict(user)

    @login_required
    def put(self):
        # ToDo: admin or self
        pass

class API_User(ApiBase):
    @login_required
    def get(self, id):
        if (not current_user.admin) and (current_user.id != id):
            abort(403, message="Admin or self only")
        user = User.query.filter_by(id=id).first()
        if user is None:
            abort(404, message="User {0} do not exist".format(id))
        return toDict(user)

api_res.add_resource(API_Users, '/users')
api_res.add_resource(API_User, '/users/<md5_id:id>')