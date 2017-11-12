'''
Created on 2016-07-25

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
from edustack.models import db
from edustack.models.course import Course, Chapter, Category
from edustack.apis.test.testApi import TestApi


class TestApiCourse(TestApi):
    def setUp(self):
        TestApi.setUp(self)
        self.testCourseName = "SetupCourseName"
        self.testCourseImage = "http://SetupCourseImage"
        self.testCourseAbout = "SetupCourseAbout"
        self.testChapterOrder = 1
        self.testChapterName = "SetupChapterName"
        self.testChapterVideoUrl = "http://SetupChapterVideoUrl"
        self.testChapterContent = "SetupChapterContent"

    def addCategory(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        ret = Category.query.filter_by(id=category.id).first()
        self.assertEqual(ret.id, category.id)
        return ret

    def addCourse(self):
        category = self.addCategory()
        course = Course(name="testCourseName",
                        image='http://testImage',
                        about='testAbout',
                        category_id=category.id)
        db.session.add(course)
        db.session.commit()
        ret = Course.query.filter_by(id=course.id).first()
        self.assertEqual(ret.id, course.id)
        return ret

    def addChapter(self):
        course = self.addCourse()
        chapter = Chapter(course.id, self.testChapterOrder,
                          self.testChapterName, self.testChapterVideoUrl,
                          self.testChapterContent)
        db.session.add(chapter)
        db.session.commit()
        ret = Chapter.query.filter_by(id=chapter.id).first()
        self.assertEqual(ret.id, chapter.id)
        return ret

class TestCategory(TestApiCourse):
    def test_getCategories(self):
        category = self.addCategory()
        response = self.client.get('/api/categories')
        self.assertEqual(response._status_code, 200)
        self.assertEqual(len(response.json['categories']), 1)
        self.assertEqual(response.json['categories'][0]['id'], category.id)
        self.assertEqual(response.json['page']['item_count'], 1)

    def test_getCategoriesEmpty(self):
        response = self.client.get("/api/categories")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['categories'], [])
    
    def test_postCategories(self):
        self.login(admin=True)
        response = self.client.post("/api/categories",
            data={'name':'testName', 'image':'http://testImage',
                  'about':'testAbout'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['name'], 'testName')

    def test_postCategoriesEmptyAbout(self):
        self.login(admin=True)
        response = self.client.post("/api/categories",
            data={'name':'testName', 'image':'http://testImage', 'about':' '})
        self.assertEqual(response._status_code, 400)

    def test_postCategoriesNotAdmin(self):
        self.login(admin=False)
        response = self.client.post("/api/categories",
            data={'name':'testName'})
        self.assertEqual(response._status_code, 403)

    def test_postCategoriesNotLogin(self):
        response = self.client.post("/api/categories",
            data={'name':'testName'})
        self.assertEqual(response._status_code, 401)

    def test_getCategory(self):
        category = self.addCategory()
        response = self.client.get("/api/categories/{0}".format(category.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], category.id)

    def test_getCategoryNotFound(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        response = self.client.get("/api/categories/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteCategory(self):
        category = self.addCategory()
        self.login(admin=True)
        response = self.client.delete("/api/categories/{0}".format(category.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], category.id)

    def test_deleteCategoryNotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.delete("/api/categories/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteCategoryNotAdmin(self):
        category = self.addCategory()
        self.login(admin=False)
        response = self.client.delete("/api/categories/{0}".format(category.id))
        self.assertEqual(response._status_code, 403)

    def test_deleteCategoryNotLogin(self):
        category = self.addCategory()
        response = self.client.delete("/api/categories/{0}".format(category.id))
        self.assertEqual(response._status_code, 401)

    def test_updateCategory(self):
        category = self.addCategory()
        self.login(admin=True)
        response = self.client.post("/api/categories/{0}".format(category.id),
            data={'name':'NewName', 'image':'testImage', 'about':'testAbout'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], category.id)
        self.assertEqual(response.json['name'], 'NewName')

    def test_upateCategoryNotAdmin(self):
        category = self.addCategory()
        self.login(admin=False)
        response = self.client.post("/api/categories/{0}".format(category.id),
            data={'name':'NewName'})
        self.assertEqual(response._status_code, 403)

    def test_updateCategoryNotLogin(self):
        category = self.addCategory()
        response = self.client.post("/api/categories/{0}".format(category.id),
            data={'name':'NewName'})
        self.assertEqual(response._status_code, 401)


class TestCourse(TestApiCourse):
    def test_getCourses(self):
        course = self.addCourse()
        response = self.client.get("/api/courses")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(len(response.json['courses']), 1)
        self.assertEqual(response.json['courses'][0]['id'], course.id)
        self.assertEqual(response.json['page']['item_count'], 1)

    def test_getCoursesEmpty(self):
        response = self.client.get("/api/courses")
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['courses'], [])

    def test_getCourse(self):
        course = self.addCourse()
        response = self.client.get("/api/courses/{0}".format(course.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], course.id)

    def test_getCourseNotFound(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        response = self.client.get("/api/courses/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_postCourses(self):
        category = self.addCategory()
        
        self.login(admin=True)
        response = self.client.post("/api/courses",
            data={'name':'testName', 'image':'http://testImage',
                  'about':'testAbout', 'category_id': category.id})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['name'], 'testName')

    def test_postCoursesEmptyAbout(self):
        category = self.addCategory()
        self.login(admin=True)
        response = self.client.post("/api/courses",
            data={'name':'testName', 'image':'http://testImage', 'about':' ',
                  'category_id': category.id})
        self.assertEqual(response._status_code, 400)

    def test_postCoursesNotAdmin(self):
        self.login(admin=False)
        response = self.client.post("/api/courses",
            data={'name':'testName'})
        self.assertEqual(response._status_code, 403)

    def test_postCoursesNotLogin(self):
        response = self.client.post("/api/courses",
            data={'name':'testName'})
        self.assertEqual(response._status_code, 401)

    def test_deleteCourse(self):
        course = self.addCourse()
        self.login(admin=True)
        response = self.client.delete("/api/courses/{0}".format(course.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], course.id)

    def test_deleteCourseNotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.delete("/api/courses/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteCourseNotAdmin(self):
        course = self.addCourse()
        self.login(admin=False)
        response = self.client.delete("/api/courses/{0}".format(course.id))
        self.assertEqual(response._status_code, 403)

    def test_deleteCourseNotLogin(self):
        course = self.addCourse()
        response = self.client.delete("/api/courses/{0}".format(course.id))
        self.assertEqual(response._status_code, 401)

    def test_updateCourse(self):
        course = self.addCourse()
        self.login(admin=True)
        response = self.client.post("/api/courses/{0}".format(course.id),
            data={'name':'NewName', 'image':'testImage', 'about':'testAbout'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], course.id)
        self.assertEqual(response.json['name'], 'NewName')

    def test_upateCourseNotAdmin(self):
        course = self.addCourse()
        self.login(admin=False)
        response = self.client.post("/api/courses/{0}".format(course.id),
            data={'name':'NewName'})
        self.assertEqual(response._status_code, 403)

    def test_updateCourseNotLogin(self):
        course = self.addCourse()
        response = self.client.post("/api/courses/{0}".format(course.id),
            data={'name':'NewName'})
        self.assertEqual(response._status_code, 401)

class TestChapter(TestApiCourse):
    def test_getChaptersCourses(self):
        chapter = self.addChapter()
        response = self.client.get("/api/chapters/courses/{0}".format(chapter.course_id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(len(response.json['chapters']), 1)
        self.assertEqual(response.json['chapters'][0]['id'], chapter.id)

    def test_getChaptersCoursesEmpty(self):
        course = self.addCourse()
        response = self.client.get("/api/chapters/courses/{0}".format(course.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['chapters'], [])

    def test_postChaptersCourses_OrderExist(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.post("/api/chapters/courses/{0}".format(chapter.course_id),
            data={'course_id':chapter.course_id,
                  'order':chapter.order,
                  'name':"testName",
                  'video_url':"testVideoUrl",
                  'content':'testContent'})
        self.assertEqual(response._status_code, 400)
        self.assertEqual(response.json['message']['order'], 'Can not duplicate!')

    def test_postChaptersCourses(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.post("/api/chapters/courses/{0}".format(chapter.course_id),
            data={'course_id':chapter.course_id,
                  'order':chapter.order+1,
                  'name':"testName",
                  'video_url':"testVideoUrl",
                  'content':'testContent'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['order'], chapter.order+1)

    def test_postChaptersCourses_Order0(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.post("/api/chapters/courses/{0}".format(chapter.course_id),
            data={'course_id':chapter.course_id,
                  'order':0,
                  'name':"testName",
                  'video_url':"testVideoUrl",
                  'content':'testContent'})
        self.assertEqual(response._status_code, 400)
        self.assertEqual(response.json['message']['order'], 'Must >= 1')

    def test_postChaptersCoursesNotLogin(self):
        course = self.addCourse()
        response = self.client.post("/api/chapters/courses/{0}".format(course.id),
            data={'course_id':course.id,
                  'order':1,
                  'name':"testName",
                  'video_url':"testVideoUrl",
                  'content':'testContent'})
        self.assertEqual(response._status_code, 401)

    def test_postChaptersCoursesNotAdmin(self):
        course = self.addCourse()
        self.login(admin=False)
        response = self.client.post("/api/chapters/courses/{0}".format(course.id),
            data={'course_id':course.id,
                  'order':1,
                  'name':"testName",
                  'video_url':"testVideoUrl",
                  'content':'testContent'})
        self.assertEqual(response._status_code, 403)

    def test_getChapter(self):
        chapter = self.addChapter()
        response = self.client.get("/api/chapters/{0}".format(chapter.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], chapter.id)

    def test_getChapterNotFound(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        response = self.client.get("/api/chapters/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_postChapters_NotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.post("/api/chapters/{0}".format(notExistId),
            data={'content':'newContent'})
        self.assertEqual(response._status_code, 404)

    def test_postChapters(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':chapter.order,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['content'], 'newContent')

    def test_postChapters_Order0(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':-1,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 400)
        self.assertEqual(response.json['message']['order'], 'Must >= 1')

    def test_postChapters_Order_Dup(self):
        chapter = self.addChapter()
        chapter2 = Chapter(chapter.course_id, chapter.order+1, chapter.name,
                          chapter.video_url, chapter.content)
        db.session.add(chapter2)
        db.session.commit()
        self.login(admin=True)
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':chapter.order,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 200)
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':chapter2.order,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 400)
        self.assertEqual(response.json['message']['order'], 'Can not duplicate!')

    def test_postChaptersNotLogin(self):
        chapter = self.addChapter()
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':chapter.order,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 401)

    def test_postChaptersNotAdmin(self):
        chapter = self.addChapter()
        self.login(admin=False)
        response = self.client.post("/api/chapters/{0}".format(chapter.id),
            data={'course_id':chapter.course.id,
                  'order':chapter.order,
                  'name':chapter.name,
                  'video_url':chapter.video_url,
                  'content':'newContent'})
        self.assertEqual(response._status_code, 403)

    def test_deleteChapter(self):
        chapter = self.addChapter()
        self.login(admin=True)
        response = self.client.delete("/api/chapters/{0}".format(chapter.id))
        self.assertEqual(response._status_code, 200)
        self.assertEqual(response.json['id'], chapter.id)

    def test_deleteChapterNotExist(self):
        notExistId = hashlib.md5("notExist").hexdigest()
        self.login(admin=True)
        response = self.client.delete("/api/chapters/{0}".format(notExistId))
        self.assertEqual(response._status_code, 404)

    def test_deleteChapterNotAdmin(self):
        chapter = self.addChapter()
        self.login(admin=False)
        response = self.client.delete("/api/chapters/{0}".format(chapter.id))
        self.assertEqual(response._status_code, 403)

    def test_deleteChapterNotLogin(self):
        chapter = self.addChapter()
        response = self.client.delete("/api/chapters/{0}".format(chapter.id))
        self.assertEqual(response._status_code, 401)


if __name__ == '__main__':
    import unittest
    unittest.main()