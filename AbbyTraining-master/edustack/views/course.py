'''
Created on 2016-09-01

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint, request, abort
from flask_login import current_user

from edustack.views import render_template
from edustack.models import get_items_by_page
from edustack.models.course import Course, Chapter
from edustack.utils import tryParse

course = Blueprint('course', __name__)


@course.route('/')
@course.route('/index/')
def index():
    pageIndex = request.args.get('page')
    pageIndex = tryParse(pageIndex, int, 1)
    courses, page = get_items_by_page(pageIndex, Course)
    return render_template(r"course/index.html", courses=courses, page=page)

@course.route('/<md5_id:course_id>/')
def getCourse(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        abort(404)
    chapters = Chapter.query.filter_by(course_id=course_id).order_by(
        Chapter.order).limit(1000)
    return render_template(r"course/course.html", course=course, chapters=chapters,
                           user=current_user)
