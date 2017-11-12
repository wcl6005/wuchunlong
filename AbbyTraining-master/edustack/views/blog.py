'''
Created on 2016-04-15

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''
import markdown2

from flask import Blueprint, request, abort
from flask_login import current_user

from edustack.views import render_template
from edustack.models import get_items_by_page
from edustack.models.blog import Blog, Comment
from edustack.utils import tryParse

blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/index/')
def index():
    pageIndex = request.args.get('page')
    pageIndex = tryParse(pageIndex, int, 1)
    blogs, page = get_items_by_page(pageIndex, Blog)
    return render_template(r"blog/index.html", blogs=blogs, page=page)

@blog.route('/<md5_id:blog_id>/')
def getBlog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()
    if blog is None:
        abort(404)
    blog.html_content = markdown2.markdown(blog.content)
    comments = Comment.query.filter_by(blog_id=blog_id).order_by(
        Comment.created_at.desc()).limit(1000)
    return render_template(r"blog/blog.html", blog=blog, comments=comments,
                           user=current_user)