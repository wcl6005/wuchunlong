from edustack.models import db, toDict
from edustack.models.course import Course, Chapter, Category
from edustack.models.test.testModel import TestModel 


class TestCategory(TestModel):
    def test_category(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        
        ret = category.query.filter_by(id=category.id).first()
        self.assertEqual(ret.name, "testCategory")

    def test_toDict(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()

        ret = category.query.filter_by(id=category.id).first()
        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["id"], category.id)
        self.assertEqual(ret["name"], "testCategory")


class TestCourse(TestModel):
    def test_course(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        
        course = Course(name="testCourseName",
                        image='http://testImage',
                        about='testAbout',
                        category_id=category.id)
        db.session.add(course)
        db.session.commit()

        ret = course.query.filter_by(id=course.id).first()
        self.assertEqual(ret.name, "testCourseName")

    def test_toDict(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        
        course = Course(name="testCourseName",
                        image='http://testImage',
                        about='testAbout',
                        category_id=category.id)
        db.session.add(course)
        db.session.commit()

        ret = course.query.filter_by(id=course.id).first()
        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["id"], course.id)
        self.assertEqual(ret["name"], "testCourseName")


class TestChapter(TestModel):
    def test_chapter(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        
        course = Course(name="testCourseName",
                        image='http://testImage',
                        about='testAbout',
                        category_id=category.id)
        db.session.add(course)
        chapter = Chapter(course.id, 1, "testChapter1", "http://testVideoUrl", "testContent")
        db.session.add(chapter)
        db.session.commit()

        ret = Chapter.query.filter_by(id=chapter.id).first()
        self.assertEqual(ret.order, 1)
        self.assertEqual(ret.name, "testChapter1")
        self.assertEqual(ret.video_url, "http://testVideoUrl")
        self.assertEqual(ret.content, "testContent")

    def test_toDict(self):
        category = Category(name='testCategory',
                            image='http://testImage', 
                            about='testAbout')
        db.session.add(category)
        db.session.commit()
        
        course = Course(name="testCourseName",
                        image='http://testImage',
                        about='testAbout',
                        category_id=category.id)
        db.session.add(course)
        chapter = Chapter(course.id, 1, "testChapter1", "http://testVideoUrl", "testContent")
        db.session.add(chapter)
        db.session.commit()

        ret = Chapter.query.filter_by(id=chapter.id).first()
        ret = toDict(ret)
        self.assertTrue("created_at" in ret)
        self.assertEqual(ret["id"], chapter.id)
        self.assertEqual(ret["order"], 1)
        self.assertEqual(ret["name"], "testChapter1")
        self.assertEqual(ret["video_url"], "http://testVideoUrl")
        self.assertEqual(ret["content"], "testContent")
        self.assertEqual(ret["course_id"], chapter.course_id)

if __name__ == '__main__':
    import unittest
    unittest.main()