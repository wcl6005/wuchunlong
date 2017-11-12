'''
Created on 2016-04-14

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''
from edustack.models.user import User
from edustack.apis.test.testApi import TestApi
import hashlib


class TestUser(TestApi):
    def test_getUsersAdmin(self):
        self.login(admin=True)
        response = self.client.get("/api/users")
        self.assertEquals(response._status_code, 200)
        self.assertEqual(len(response.json["users"]), 1)
        self.assertEqual(response.json["users"][0]["email"], self.testUserEmail)

    def test_getUsersNotAdmin(self):
        self.login()
        response = self.client.get("/api/users")
        self.assertEquals(response._status_code, 403)

    def test_getUsersNotLogin(self):
        response = self.client.get("/api/users")
        self.assertEquals(response._status_code, 401)

    def test_postUsers(self):
        testEmail = "testUserEmail@postUsers.com"
        testPassword = hashlib.md5("testPassword").hexdigest()
        response = self.client.post("/api/users",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              name='testUserName')
                                    )
        self.assertEquals(response._status_code, 200)

    def test_postUsersDuplicate(self):
        testEmail = "testUserEmail@postUsers.com"
        testPassword = hashlib.md5("testPassword").hexdigest()
        response = self.client.post("/api/users",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              name='testUserName')
                                    )
        self.assertEquals(response._status_code, 200)
        response = self.client.post("/api/users",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              name='testUserName')
                                    )
        self.assertEquals(response._status_code, 400)

    def test_postUsersErrEmail(self):
        testEmail = "testUserEmail"
        testPassword = hashlib.md5("testPassword").hexdigest()
        response = self.client.post("/api/users",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              name='testUserName')
                                    )
        self.assertEquals(response._status_code, 400)
        self.assertTrue('email' in response.json['message'].lower())

    def test_postUsersErrPassword(self):
        testEmail = 'testUserEmail@postUsers.com'
        testPassword = 'testPassword'
        response = self.client.post("/api/users",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              name='testUserName')
                                    )
        self.assertEquals(response._status_code, 400)
        self.assertTrue('password' in response.json['message'].lower())

    def test_getUserNotValid(self):
        fakeid = "1"*50
        response = self.client.get("/api/users/"+fakeid)
        self.assertEquals(response._status_code, 401)

    def test_getUserNotFound(self):
        self.login(admin=True)

        response = self.client.get("/api/users/notexist")
        self.assertEquals(response._status_code, 404)
        self.assertFalse(hasattr(response, 'json'))
        fakeid = "1"*50
        response = self.client.get("/api/users/"+fakeid)
        self.assertEquals(response._status_code, 404)
        self.assertEquals(response.json['message'], "User {0} do not exist".format(fakeid))

    def test_getUserSelf(self):
        self.login()
        user = User.query.filter_by(email=self.testUserEmail).first()

        response = self.client.get("/api/users/{0}".format(user.id))
        self.assertEquals(response._status_code, 200)
        self.assertEqual(response.json["id"], user.id)

    def test_getUserAdmin(self):
        self.login(admin=True)
        user = User.query.filter_by(email=self.testUserEmail).first()

        response = self.client.get("/api/users/{0}".format(user.id))
        self.assertEquals(response._status_code, 200)
        self.assertEqual(response.json["id"], user.id)

    def test_getUserNonAdminSelf(self):
        self.addUser()
        self.login(email="testNonSelfAdminUser@email.com")
        user = User.query.filter_by(email=self.testUserEmail).first()
        response = self.client.get("/api/users/{0}".format(user.id))
        self.assertEquals(response._status_code, 403)


if __name__ == '__main__':
    import unittest
    unittest.main()