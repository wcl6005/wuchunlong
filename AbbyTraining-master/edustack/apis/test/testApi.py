'''
Created on 2016-04-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''
import hashlib
from flask_testing import TestCase

from edustack import wsgiApp
from edustack.apis import addArg, ApiBase, api_res
from edustack.models import db
from edustack.models.user import User, LocalAuth
from edustack.models.blog import Blog, Comment
from flask_restful.reqparse import Argument

class TestApi(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://test.sqlite"
    TESTING = True

    def create_app(self):
        return wsgiApp

    def setUp(self):
        db.create_all()
        self.testUserEmail = "testApiSetup@test.com".lower()
        self.testUserPassword = hashlib.md5(self.testUserEmail).hexdigest()
        self.testUserName = "testApiSetupName"
        self.testUserImage = "http://testApiSetupImage.com"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def addUser(self, email=None, password=None, admin=False):
        if email is None:
            email = self.testUserEmail
        email = email.lower()
        if password is None:
            password = self.testUserPassword
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(self.testUserName, email, self.testUserImage, admin)
            db.session.add(user)
            localAuth = LocalAuth(user.id, password)
            db.session.add(localAuth)
            db.session.commit()
        user = User.query.filter_by(email=email).first()
        user.admin = admin
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        self.assertEqual(admin, user.admin)
        return user

    def login(self, email=None, password=None, admin=False):
        if email is None:
            email = self.testUserEmail
        email = email.lower()
        if password is None:
            password = self.testUserPassword
        self.addUser(email, password, admin)
        user = User.query.filter_by(email=email).first()
        self.assertEqual(user.email, email)

        return self.client.post("/api/signin",
                                data=dict(email=email,
                                          password=password,
                                          remember="true")
                                )

    def logout(self):
        return self.client.get("/api/signout")

class TestCommon(TestApi):
    def test_API_getArgs(self):
        a1 = Argument('a1', default='Default', case_sensitive=False, trim=True)
        a2 = Argument('a2', type=int, required=True, help='help_a2')
        a3 = Argument('a3', type=int, required=True, help='help_a3')
        a4 = Argument('a4', default=False, type=bool)
        @addArg(aList=[a1, a2, a3, a4])
        class TestClass(ApiBase):
            def post(self):
                args = self.getArgs('aList')
                self.abortIfArgsEmpty(args, [a1])
                return [args['a1'], args['a2'], args['a3'], args['a4']]
        api_res.add_resource(TestClass, '/test')

        ret = self.client.post("/api/test",data=dict(a1="a1 ", a2=' 2', a3=2))
        self.assertEqual(ret.json, ['a1', 2, 2, False])

        ret = self.client.post("/api/test", data=dict())
        self.assertEqual(ret._status_code, 400)
        self.assertEqual(len(ret.json['message']), 1)
        self.assertEqual(ret.json['message']['a2'], 'help_a2')

        ret = self.client.post("/api/test", data=dict(a1=" ", a2=' 2', a3=2))
        self.assertEqual(ret._status_code, 400)
        self.assertEqual(len(ret.json['message']), 1)
        self.assertEqual(ret.json['message']['a1'], 'Can not be empty!')

        ret = self.client.post("/api/test", data=dict(a2=2, a3=2, a4='true'))
        self.assertTrue(ret.json[3])

        # Be careful!!!
        ret = self.client.post("/api/test", data=dict(a2=2, a3=2, a4='false'))
        self.assertTrue(ret.json[3])

    def test_addArg_single(self):
        testList = ['a1', Argument('a2')]
        @addArg(aList=testList)
        class TestClass(object):
            def testFun(self):
                return self.argDict

        ret = TestClass().testFun()
        self.assertEqual(testList[0], ret['aList'].args[0].name)
        self.assertEqual(testList[1], ret['aList'].args[1])

    def test_addArg_multi_1(self):
        testList = ['a1', 'a2', 'a3']
        @addArg(aList=testList, bList=testList)
        class TestClass(object):
            def testFun(self):
                return self.argDict

        ret = TestClass().testFun()
        self.assertEqual(testList, map(lambda x:x.name, ret['aList'].args))
        self.assertEqual(testList, map(lambda x:x.name, ret['bList'].args))

    def test_addArg_multi_2(self):
        testList = ['a1', 'a2', 'a3']
        @addArg(bList=testList, cList=testList)
        @addArg(aList=testList)
        class TestClass(object):
            def testFun(self):
                return self.argDict

        ret = TestClass().testFun()
        self.assertEqual(testList, map(lambda x:x.name, ret['aList'].args))
        self.assertEqual(testList, map(lambda x:x.name, ret['bList'].args))
        self.assertEqual(testList, map(lambda x:x.name, ret['cList'].args))

if __name__ == '__main__':
    import unittest
    unittest.main()