'''
Created on 2016-07-25

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask_restful import abort
from flask_login import login_required, current_user
from edustack.models.course import Course, Chapter, Category
from edustack.models import toDict, get_items_by_page, db
from edustack.apis import addArg, ApiBase, api_res, ArgPage, ArgFormat
from flask_restful.reqparse import Argument


ArgCategoryName = Argument('name', required=True, trim=True,
                           help='Invalid name')
ArgCategoryImage = Argument('image', required=True, trim=True,
                            help='Invalid image')
ArgCategoryAbout = Argument('about', required=True, trim=True,
                            help='Invalid about')

@addArg(getCategory=[ArgPage, ArgFormat])
@addArg(postCategory=[ArgCategoryName, ArgCategoryImage, ArgCategoryAbout])
class API_Categories(ApiBase):
    def get(self):
        args = self.getArgs('getCategory')
        _page, _format = args['page'], args['format']

        categories, page = get_items_by_page(_page, Category)
        
        return dict(categories=[toDict(i) for i in categories],
                    page=page.toDict())

    @login_required
    def post(self):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postCategory')

        self.abortIfArgsEmpty(args, [ArgCategoryName, ArgCategoryImage,
                                     ArgCategoryAbout])

        category = Category(*(args[i.name] for i in [ArgCategoryName,
            ArgCategoryImage, ArgCategoryAbout]))

        db.session.add(category)
        db.session.commit()
        ret = Category.query.filter_by(id=category.id).first()
        return toDict(ret)

@addArg(postCategory=[ArgCategoryName, ArgCategoryImage, ArgCategoryAbout])
class API_Category(ApiBase):
    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if category is None:
            abort(404, message="Category {0} do not exist.".format(id))
        return toDict(category)

    @login_required
    def delete(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        category = Category.query.filter_by(id=id).first()
        if category is None:
            abort(404, message="Category {0} do not exist.".format(id))
        db.session.delete(category)
        db.session.commit()
        return toDict(category)

    @login_required
    def post(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postCategory')
 
        self.abortIfArgsEmpty(args, [ArgCategoryName, ArgCategoryImage, ArgCategoryAbout])
 
        kwargs = {i.name:args[i.name] for i in 
                  [ArgCategoryName, ArgCategoryImage, ArgCategoryAbout]}
        Category.query.filter_by(id=id).update(kwargs)
        db.session.commit()
        category = Category.query.filter_by(id=id).first()
        return toDict(category)

ArgCourseName = Argument('name', required=True, trim=True,
                         help='Invalid name')
ArgCourseImage = Argument('image', required=True, trim=True,
                          help='Invalid image')
ArgCourseAbout = Argument('about', required=True, trim=True,
                          help='Invalid about')
ArgCourseCourseId = Argument('category_id', required=True, trim=True,
                             help='Invalid category_id')

@addArg(getCourse=[ArgPage, ArgFormat])
@addArg(postCourse=[ArgCourseName, ArgCourseImage, ArgCourseAbout, ArgCourseCourseId])
class API_Courses(ApiBase):
    def get(self):
        args = self.getArgs('getCourse')
        _page, _format = args['page'], args['format']

        courses, page = get_items_by_page(_page, Course)
        
        return dict(courses=[toDict(i) for i in courses],
                    page=page.toDict())

    @login_required
    def post(self):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postCourse')

        self.abortIfArgsEmpty(args, [ArgCourseName, ArgCourseImage,
                                     ArgCourseAbout, ArgCourseCourseId])

        course = Course(*(args[i.name] for i in 
                          [ArgCourseName, ArgCourseImage, ArgCourseAbout,
                           ArgCourseCourseId]))

        db.session.add(course)
        db.session.commit()
        ret = Course.query.filter_by(id=course.id).first()
        return toDict(ret)

@addArg(postCourse=[ArgCourseName, ArgCourseImage, ArgCourseAbout])
class API_Course(ApiBase):
    def get(self, id):
        course = Course.query.filter_by(id=id).first()
        if course is None:
            abort(404, message="Course {0} do not exist.".format(id))
        return toDict(course)

    @login_required
    def delete(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        course = Course.query.filter_by(id=id).first()
        if course is None:
            abort(404, message="Course {0} do not exist.".format(id))
        db.session.delete(course)
        db.session.commit()
        return toDict(course)

    @login_required
    def post(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postCourse')

        self.abortIfArgsEmpty(args, [ArgCourseName, ArgCourseImage, ArgCourseAbout])

        kwargs = {i.name:args[i.name] for i in [ArgCourseName, ArgCourseImage, ArgCourseAbout]}
        Course.query.filter_by(id=id).update(kwargs)
        db.session.commit()
        course = Course.query.filter_by(id=id).first()
        return toDict(course)

ArgChapterCourseId = Argument('course_id', required=True, trim=True, help='Invalid course_id')
ArgChapterOrder = Argument('order', required=True, trim=True, help='Invalid order', type=int)
ArgChapterName = Argument('name', required=True, trim=True, help='Invalid name')
ArgChapterVideoUrl = Argument('video_url', default='', trim=True, help='Invalid video_url')
ArgChapterContent = Argument('content', default='', trim=True, help='Invalid content')

def checkPostChapter(course_id, order, chapter_id=None):
        course = Course.query.filter_by(id=course_id).first()
        if not course:
            abort(400, message={ArgChapterCourseId.name: "Course {0} do not exist.".format(id)})

        if order <= 0:
            abort(400, message={ArgChapterOrder.name: "Must >= 1"})

        chapters = Chapter.query.filter_by(course_id=course_id).filter_by(
            order=order).all()
        if id:
            chapters = [i for i in chapters if i.id != chapter_id]

        if len(chapters) > 0:
            abort(400, message={ArgChapterOrder.name: "Can not duplicate!"})


@addArg(postChapter=[ArgChapterCourseId, ArgChapterOrder, ArgChapterName,
                     ArgChapterVideoUrl, ArgChapterContent])
class API_Chapter(ApiBase):
    def get(self, id):
        chapter = Chapter.query.filter_by(id=id).first()
        if chapter is None:
            abort(404, message="Chapter {0} do not exist.".format(id))
        return toDict(chapter)

    @login_required
    def delete(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        chapter = Chapter.query.filter_by(id=id).first()
        if chapter is None:
            abort(404, message="Chapter {0} do not exist.".format(id))
        db.session.delete(chapter)
        db.session.commit()
        return toDict(chapter)

    @login_required
    def post(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postChapter')

        chapter = Chapter.query.filter_by(id=id).first()
        if not chapter:
            abort(404, message="Chapter {0} do not exist.".format(id))

        self.abortIfArgsEmpty(args, [ArgChapterCourseId, ArgChapterName])
        checkPostChapter(args[ArgChapterCourseId.name],
                         args[ArgChapterOrder.name], id)

        kwargs = {i.name:args[i.name] for i in [ArgChapterCourseId,
                                                ArgChapterOrder,
                                                ArgChapterName,
                                                ArgChapterVideoUrl,
                                                ArgChapterContent]}
        Chapter.query.filter_by(id=id).update(kwargs)
        
        db.session.commit()
        chapter = Chapter.query.filter_by(id=id).first()
        return toDict(chapter)


@addArg(postChapter=[ArgChapterOrder, ArgChapterName,
                     ArgChapterVideoUrl, ArgChapterContent])
class API_Chapters(ApiBase):
    def get(self, id):
        chapters = Chapter.query.filter_by(course_id=id).all()
        return dict(chapters=[toDict(i) for i in chapters])

    @login_required
    def post(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postChapter')

        self.abortIfArgsEmpty(args, [ArgChapterName])
        checkPostChapter(id, args[ArgChapterOrder.name])

        kwargs = {i.name:args[i.name] for i in [ArgChapterOrder,
                                                ArgChapterName,
                                                ArgChapterVideoUrl,
                                                ArgChapterContent]}
        chapter = Chapter(course_id=id, **kwargs)

        db.session.add(chapter)
        db.session.commit()
        chapter = Chapter.query.filter_by(id=chapter.id).first()
        return toDict(chapter)

api_res.add_resource(API_Categories, '/categories')
api_res.add_resource(API_Category, '/categories/<md5_id:id>')
api_res.add_resource(API_Courses, '/courses')
api_res.add_resource(API_Course, '/courses/<md5_id:id>')
api_res.add_resource(API_Chapters, '/chapters/courses/<md5_id:id>')
api_res.add_resource(API_Chapter, '/chapters/<md5_id:id>')