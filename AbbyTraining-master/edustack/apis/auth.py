'''
Created on 2016-04-12

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import flask_login as login

from flask_restful import abort

from edustack.models import toDict
from edustack.models.user import User
from edustack.models.user import LocalAuth
from edustack.apis import api_res, addArg, ApiBase, ArgEmail, ArgPassword,\
    ArgRemember
from flask_login import logout_user


@addArg(postAuth=[ArgEmail, ArgPassword, ArgRemember])
class API_Auth(ApiBase):
    def post(self):
        args = self.getArgs('postAuth')
        remember = args['remember']=='true'

        user = User.query.filter_by(email=args['email']).first()
        if not user:
            abort(401, message="Invalid email.")
        
        localAuth = LocalAuth.query.filter_by(user_id=user.id).first()
        if args['password'] != localAuth.password:
            abort(401, message="Invalid password.")

        login.login_user(user, remember=remember)
        return toDict(user)

class API_Logout(ApiBase):
    def get(self):
        logout_user()
        return {}

api_res.add_resource(API_Auth, '/signin')
api_res.add_resource(API_Logout, '/signout')
