from edustack.models.test.testModel import TestModel
from edustack.models.user import User
from edustack.models.user import LocalAuth
from edustack.models import db
from edustack.models import toDict


class TestUser(TestModel):
    def test_userNotFound(self):
        ret = User.query.filter_by(id="notFound").first()
        self.assertTrue(ret is None)

    def test_userCreate(self):
        testEmail = "testEmail@test.com".upper()
        user = User("testUser", testEmail, "http://testImage.com")
        db.session.add(user)
        db.session.commit()

        ret = User.query.filter_by(id=user.id).first()
        self.assertEqual(ret.name, user.name)
        self.assertEqual(ret.email, testEmail.lower())

    def test_toDict(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)
        db.session.commit()
        ret = User.query.filter_by(id=user.id).first()

        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["name"], user.name)


class TestLocalAuth(TestModel):
    def test_localAuth(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)

        testPassword = "testPassword"
        localAuth = LocalAuth(user.id, testPassword)
        db.session.add(localAuth)
        db.session.commit()

        retLocalAuth = LocalAuth.query.filter_by(id=localAuth.id).first()
        self.assertEqual(retLocalAuth.password, testPassword)

if __name__ == '__main__':
    import unittest
    unittest.main()