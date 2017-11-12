import datetime
import time
from flask_testing import TestCase

from edustack.models import db, isJsonable, toDict, toJsonTime, toDictExt,\
    FieldMixin
from edustack import wsgiApp


class TestModel(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://test.sqlite"
    TESTING = True

    def create_app(self):
        return wsgiApp

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestCommon(TestModel):
    def test_isJsonable_False(self):
        ret = isJsonable(datetime.datetime.now())
        self.assertFalse(ret)

    def test_isJsonable_True(self):
        ret = isJsonable(5)
        self.assertTrue(ret)

    def test_toJsonTime(self):
        timeObj = datetime.datetime(1990, 1, 1)
        ret = toJsonTime(timeObj)
        expTuple = (1990, 1, 1, 0, 0, 0, 0, 0, 0)
        self.assertEqual(ret, time.mktime(expTuple))

    def test_toDictNone(self):
        ret = toDict(None)
        self.assertEqual(ret, {})

    def test_toDict(self):
        class TestClass(FieldMixin):
            def __init__(self):
                self.fieldA = 3
                self.fieldB = datetime.datetime.now()
                self.fieldC = datetime.datetime.now()
            
            _jsonMapDict = FieldMixin._jsonMapDict.copy()
            _jsonMapDict['fieldB'] = toJsonTime
            _jsonMapDict['notExist'] = str
            
        ret = toDict(TestClass())
        self.assertTrue("fieldA" in ret)
        self.assertTrue("fieldB" in ret)
        self.assertFalse("fieldC" in ret)
        self.assertFalse("notExist" in ret)

    def test_toDictExt(self):
        class TestClass():
            def __init__(self):
                self.fieldA = 3
                self.fieldB = 3
            
        ret = toDictExt("fieldA")(TestClass())
        self.assertTrue("fieldA" in ret)
        self.assertFalse("fieldB" in ret)

if __name__ == '__main__':
    import unittest
    unittest.main()