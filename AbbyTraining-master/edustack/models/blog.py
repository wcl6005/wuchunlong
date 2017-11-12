'''
Created on 2016-04-12

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''
import datetime
from edustack.models import db, FieldMixin
from edustack.utils import next_id

class Blog(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'))
    name = db.Column(db.String(50))
    summary = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')

    _regexMapDict = FieldMixin._regexMapDict.copy()

    def __init__(self, user_id, name, summary, content):
        self.id = next_id()
        self.user_id = user_id
        self.name = name
        self.summary = summary
        self.content = content

    def __repr__(self):
        return '<Blog {!r}>'.format(self.name)

class Comment(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'))
    blog_id = db.Column(db.String(50), db.ForeignKey('blog.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, user_id, blog_id, content):
        self.id = next_id()
        self.user_id = user_id
        self.blog_id = blog_id
        self.content = content

    def __repr__(self):
        return '<Comment {!r}>'.format(self.content)