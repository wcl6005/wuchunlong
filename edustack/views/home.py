# -*- coding: utf-8 -*-
'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template, redirect, request, url_for
from flask_login import current_user, logout_user
from edustack.models import User
from edustack.models import Blog
from edustack.views.api import _get_blogs_by_page

from edustack.models import Playvideo

home = Blueprint('home', __name__)

def _get_page_index():
    pageIndex = request.args.get('page', '1')
    try:
        pageIndex = int(pageIndex)
    except:
        pageIndex = 1
    return pageIndex

@home.route('/')
@home.route('/index/')
def index():
    pageIndex = _get_page_index()
    blogs, page = _get_blogs_by_page(pageIndex)
    return render_template(r"home/blogs.html", blogs=blogs, page=page)

@home.route('/register/')
def register():
    return render_template(r"home/register.html")

@home.route('/signin/')
def signin():
    return render_template(r"home/signin.html")

@home.route('/signout/')
def signout():
    logout_user()
    return redirect(url_for('home.index'))

@home.route('/')
@home.route('/regplay/')
def mregplay():
    return render_template(r"home/regplay.html")
