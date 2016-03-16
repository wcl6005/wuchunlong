# -*- coding: utf-8 -*-

'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint
from flask import render_template
from edustack.models import User
from edustack.models import Blog
from edustack.models import Comment
from edustack.models import Playvideo

test = Blueprint('test', __name__)

#  http://localhost:5000/test/smoketest/
@test.route('/')
@test.route('/smoketest/')
def hello():
    users = User.query.all()
    blogs = Blog.query.all()
    comments = Comment.query.all()
    return render_template(r"test/smoketest.html",users=users,
                           blogs=blogs, comments=comments)
    
#  http://localhost:5000/test/test/
@test.route('/')
@test.route('/test/')
def mtest():

	playvideos = Playvideo.query.all()
	#playvideos =[{'playnume':u'中国','intvideo':u'人民'}]  #ok
	return render_template(r"test/test.html",playvideos=playvideos)
