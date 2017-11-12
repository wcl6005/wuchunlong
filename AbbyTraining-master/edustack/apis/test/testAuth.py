'''
Created on 2016-04-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from edustack.apis.test.testApi import TestApi


class TestAuth(TestApi):
    def test_login_ok(self):
        response = self.login()
        self.assertEquals(response._status_code, 200)
        self.assertTrue("Set-Cookie" in str(response.headers))

    def test_login_missArg(self):
        response = self.client.post("/api/signin",
                                    data=dict(email="testEmail",
                                              wrongArg="WrongArg")
                                    )
        self.assertEquals(response._status_code, 400)

    def test_login_nok(self):
        testEmail = "admin@test.com"
        testPassword = "WrongPassword"
        response = self.client.post("/api/signin",
                                    data=dict(email=testEmail,
                                              password=testPassword,
                                              remember="true")
                                    )
        self.assertEquals(response._status_code, 401)

    def test_logout(self):
        response = self.logout()
        self.assertEquals(response._status_code, 200)
        self.assertTrue("Set-Cookie" not in str(response.headers))

if __name__ == '__main__':
    import unittest
    unittest.main()