'''
Created on 2016-04-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from edustack.models import db, toDict
from edustack.models.user import User
from edustack.models.blog import Blog, Comment
from edustack.models.test.testModel import TestModel 


class TestBlog(TestModel):
    def test_blog(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)
        blog = Blog(user.id, "testName", "testSummary", "testContent")
        db.session.add(blog)
        db.session.commit()

        ret = Blog.query.filter_by(id=blog.id).first()
        self.assertEqual(user.id, ret.user_id)

    def test_toDict(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)
        blog = Blog(user.id, "testName", "testSummary", "testContent")
        db.session.add(blog)
        db.session.commit()

        ret = Blog.query.filter_by(id=blog.id).first()
        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["id"], blog.id)
        self.assertTrue("id" not in ret["user"])
        self.assertEqual(ret["user"]["name"], user.name)


class TestComment(TestModel):
    def test_comment(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)
        blog = Blog(user.id, "testName", "testSummary", "testContent")
        db.session.add(blog)
        comment = Comment(user.id, blog.id, "testContent")
        db.session.add(comment)
        db.session.commit()

        ret = Comment.query.filter_by(id=comment.id).first()
        self.assertEqual(ret.id, comment.id)

    def test_toDict(self):
        user = User("testUser", "testEmail@test.com", "http://testImage.com")
        db.session.add(user)
        blog = Blog(user.id, "testName", "testSummary", "testContent")
        db.session.add(blog)
        comment = Comment(user.id, blog.id, "testContent")
        db.session.add(comment)
        db.session.commit()

        ret = Comment.query.filter_by(id=comment.id).first()
        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["id"], comment.id)
        self.assertTrue("id" not in ret["user"])
        self.assertEqual(ret["user"]["name"], user.name)

if __name__ == '__main__':
    import unittest
    unittest.main()