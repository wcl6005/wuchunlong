import datetime

from edustack.models import db, FieldMixin
from edustack.utils import next_id


class Category(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(120))
    image = db.Column(db.String(1024))
    about = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    courses = db.relationship('Course', backref='category', lazy='dynamic')
    
    def __init__(self, name, image, about):
        self.id = next_id()
        self.name = name
        self.image = image
        self.about = about

    def __repr__(self):
        return '<Category {!r}>'.format(self.name)

class Course(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(120))
    image = db.Column(db.String(1024))
    about = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    category_id = db.Column(db.String(50), db.ForeignKey('category.id'))
    chapters = db.relationship('Chapter', backref='course', lazy='dynamic')

    def __init__(self, name, image, about, category_id):
        self.id = next_id()
        self.name = name
        self.image = image
        self.about = about
        self.category_id = category_id

    def __repr__(self):
        return '<Course {!r}>'.format(self.name)

class Chapter(db.Model, FieldMixin):
    id = db.Column(db.String(50), primary_key=True)
    order = db.Column(db.Integer)
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'))
    video_url = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, course_id, order, name, video_url, content):
        self.id = next_id()
        self.order = order
        self.course_id = course_id
        self.name = name
        self.video_url = video_url
        self.content = content

    def __repr__(self):
        return '<Chapter {!r}>'.format(self.name)