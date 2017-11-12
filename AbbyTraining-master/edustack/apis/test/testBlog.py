'''
Created on 2016-04-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
from edustack.models import db
from edustack.models.blog import Blog, Comment
from edustack.apis.test.testApi import TestApi

class TestApiBlog(TestApi):
    def setUp(self):
        TestApi.setUp(self)
        self.testBlogName = "SetupBlogName"
        self.testBlogSummary = "SetupBlogSummary"
        self.testBlogContent = "SetupBlogContent"
        self.testCommentContent = "SetupCommentContent"

    def addBlog(self):
        user = self.addUser(admin=True)
        blog = Blog(user.id, self.testBlogName, self.testBlogSummary,
                    self.testBlogContent)
        db.session.add(blog)
        db.session.commit()
        ret = Blog.query.filter_by(id=blog.id).first()
        self.assertEqual(ret.id, blog.id)
        return ret

    def addComment(self):
        user = self.addUser(admin=True)
        blog = self.addBlog()
        comment = Comment(user.id, blog.id, self.testCommentContent)
        db.session.add(comment)
        db.session.commit()
        ret = Comment.query.filter_by(id=comment.id).first()
        self.assertEqual(ret.id, comment.id)
        return ret


class TestBlog(TestApiBlog):
    def test_getBlogs(self):
        blog = self.addBlog()
        response = self.client.get("/api/blogs")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(len(response.json['blogs']), 1)
        self.assertEqual(response.json['blogs'][0]['id'], blog.id)
        self.assertEqual(response.json['page']['item_count'], 1)

    def test_getBlogsEmpty(self):
        response = self.client.get("/api/blogs")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['blogs'], [])

    def test_getBlog(self):
        blog = self.addBlog()
        response = self.client.get("/api/blogs/{0}".format(blog.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], blog.id)

    def test_getBlogNotFound(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        response = self.client.get("/api/blogs/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_postBlogs(self):
        userRet = self.login(admin=True)
        response = self.client.post("/api/blogs",
            data={'name':'testName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['user_id'], userRet.json['id'])

    def test_postBlogsNotAdmin(self):
        self.login(admin=False)
        response = self.client.post("/api/blogs",
            data={'name':'testName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 403)

    def test_postBlogsNotLogin(self):
        response = self.client.post("/api/blogs",
            data={'name':'testName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 401)

    def test_deleteBlog(self):
        blog = self.addBlog()
        self.login(admin=True)
        response = self.client.delete("/api/blogs/{0}".format(blog.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], blog.id)

    def test_deleteBlogNotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.delete("/api/blogs/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteBlogNotAdmin(self):
        blog = self.addBlog()
        self.login(admin=False)
        response = self.client.delete("/api/blogs/{0}".format(blog.id))
        self.assertEqual(response._status_code, 403)

    def test_deleteBlogNotLogin(self):
        blog = self.addBlog()
        response = self.client.delete("/api/blogs/{0}".format(blog.id))
        self.assertEqual(response._status_code, 401)

    def test_updateBlog(self):
        blog = self.addBlog()
        self.login(admin=True)
        response = self.client.post("/api/blogs/{0}".format(blog.id),
            data={'name':'NewName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], blog.id)
        self.assertEqual(response.json['name'], 'NewName')

    def test_upateBlogsNotAdmin(self):
        blog = self.addBlog()
        self.login(admin=False)
        response = self.client.post("/api/blogs/{0}".format(blog.id),
            data={'name':'NewName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 403)

    def test_updateBlogsNotLogin(self):
        blog = self.addBlog()
        response = self.client.post("/api/blogs/{0}".format(blog.id),
            data={'name':'NewName', 'summary':'testSummary',
                  'content':'testContent'})
        self.assertEqual(response._status_code, 401)

class TestComment(TestApiBlog):
    def test_getComments(self):
        comment = self.addComment()
        response = self.client.get("/api/comments")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(len(response.json['comments']), 1)
        self.assertEqual(response.json['comments'][0]['id'], comment.id)
        self.assertEqual(response.json['page']['item_count'], 1)

    def test_getCommentsEmpty(self):
        response = self.client.get("/api/comments")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['comments'], [])

    def test_getComment(self):
        comment = self.addComment()
        response = self.client.get("/api/comments/{0}".format(comment.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], comment.id)

    def test_getCommentNotFound(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        response = self.client.get("/api/comments/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_postComments(self):
        blog = self.addBlog()
        userRet = self.login()
        response = self.client.post("/api/comments/{0}".format(blog.id),
            data={'content':'testContent'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['user_id'], userRet.json['id'])

    def test_postCommentsNotLogin(self):
        blog = self.addBlog()
        response = self.client.post("/api/comments/{0}".format(blog.id),
            data={'content':'testContent'})
        self.assertEqual(response._status_code, 401)

    def test_deleteComment(self):
        comment = self.addComment()
        self.login(admin=True)
        response = self.client.delete("/api/comments/{0}".format(comment.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], comment.id)

    def test_deleteCommentNotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.delete("/api/comments/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteCommentNotAdmin(self):
        comment = self.addComment()
        self.login(admin=False)
        response = self.client.delete("/api/comments/{0}".format(comment.id))
        self.assertEqual(response._status_code, 403)

    def test_deleteCommentNotLogin(self):
        comment = self.addComment()
        response = self.client.delete("/api/comments/{0}".format(comment.id))
        self.assertEqual(response._status_code, 401)


if __name__ == '__main__':
    import unittest
    unittest.main()