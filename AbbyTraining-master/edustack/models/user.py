'''
Created on 2016-01-13

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import datetime

from edustack.models import db, FieldMixin
from edustack.models.blog import Blog, Comment
from edustack.utils import next_id

class User(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    admin = db.Column(db.Boolean)
    image = db.Column(db.String(500))

    localauths = db.relationship('LocalAuth', backref='user', lazy='dynamic')
    students = db.relationship('Student', backref='user', lazy='dynamic')
    instructors = db.relationship('Instructor', backref='user', lazy='dynamic')
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __init__(self, name, email, image, admin=False):
        self.id = next_id()
        self.name = name
        self.email = email.lower()
        self.image = image
        self.admin = admin

    def __repr__(self):
        return '<User {!r}>'.format(self.name)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.name

class LocalAuth(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(120))
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'))

    def __init__(self, user_id, password):
        self.id = next_id()
        self.user_id = user_id
        self.password = password

    def __repr__(self):
        return '<LocalAuth {!r}>'.format(self.user)

class Student(db.Model, FieldMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, userId):
        self.user_id = userId

    def __repr__(self):
        return '<Student {!r}>'.format(self.user)

class Instructor(db.Model, FieldMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, userId):
        self.user_id = userId

    def __repr__(self):
        return '<Instructor {!r}>'.format(self.user)