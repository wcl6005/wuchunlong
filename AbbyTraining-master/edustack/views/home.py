'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from flask import Blueprint, redirect, url_for
from flask_login import logout_user
from edustack.views import render_template

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/index/')
def index():
    return render_template(r"home/index.html")

@home.route('/signin/')
def signin():
    return render_template(r"home/signin.html")

@home.route('/signout/')
def signout():
    logout_user()
    return redirect(url_for('home.index'))

@home.route('/register/')
def register():
    return render_template(r"home/register.html")