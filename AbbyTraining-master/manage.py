'''
Created on 2016-01-17

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import hashlib
import logging
import os
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("manage.py")
global app

def showUsage():
    print("""Usage:
    python manage.py <Option>
    python manage.py syncdb    # Create DB
    python manage.py init      # Init Demo datas
    python manage.py clean     # Clean virtenv
    python manage.py prepare   # Prepare virtenv
    """)
    sys.exit()

def opt_syncdb():
    from edustack.models import db
    db.drop_all()
    db.create_all()

def opt_init():
    from edustack.models import db
    from edustack.models.user import LocalAuth, User
    from edustack.models.blog import Blog, Comment
    from edustack.models.course import Course, Chapter, Category

    def add_local_user(name, email, admin=False):
        emailHash = hashlib.md5(email).hexdigest()
        image = r"http://www.gravatar.com/avatar/{0}?d=mm&s=120".format(emailHash)
        if admin:
            image = r"http://tp3.sinaimg.cn/2804214754/180/5668812169/1"
        db.session.add(User(name, email, image, admin))
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        db.session.add(LocalAuth(user.id, password=emailHash))
        db.session.commit()
        return user

    adminUser = add_local_user("admin", "admin@test.com", admin=True)
    add_local_user("test1", "test1@test.com")
    add_local_user("test2", "test2@test.com")

    blogStr = """
An h1 header
============

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, and `monospace`. Itemized lists
look like:

  * this one
  * that one
  * the other one

and images can be specified like so:

![example image](http://www.unexpected-vortices.com/sw/rippledoc/example-image.jpg "An exemplary image")
    """

    for i in range(6):
        blog = Blog(user_id = adminUser.id,
                    name = "Markdown2 Example {0}".format(i),
                    summary = "Example about Markdown blog {0}".format(i),
                    content = blogStr)
        db.session.add(blog)
        comment = Comment(adminUser.id, blog.id, "http://www.unexpected-"
            "vortices.com/sw/rippledoc/quick-markdown-example.html")
        db.session.add(comment)

    db.session.commit()

    for i in range(5):
        category = Category(name='Category {0}'.format(i),
                            image='http://7xudfs.com1.z0.glb.clouddn.com/Test-f4f338218d4245cf8fad114381f0e30a-CloudTools.png',
                            about='Test About Category')
        db.session.add(category)
        db.session.commit()
        for j in range(12):
            course = Course(name='Course {0}'.format(j),
                            image='http://7xudfs.com1.z0.glb.clouddn.com/Test-f4f338218d4245cf8fad114381f0e30a-CloudTools.png',
                            about='Test About Text',
                            category_id=category.id)
            db.session.add(course)
            db.session.commit()
            for k in range(1, 9):
                chapter = Chapter(course_id=course.id,
                                  order=k,
                                  name='Chapter {0}'.format(k),
                                  video_url='http://7xudfs.com1.z0.glb.clouddn.com/Test-f4f338218d4245cf8fad114381f0e30a-sport.mp4',
                                  content='Test Chapter Content')
                db.session.add(chapter)
                db.session.commit()

    db.session.commit()

def opt_clean():
    ENV_DIR = "env"
    if os.path.isdir(ENV_DIR):
        shutil.rmtree(ENV_DIR)

def opt_test():
    pass

def opt_prepare():
    _assert_cmd_exist("pip")
    os.system("pip install virtualenv")

    INSTANCE_DIR = "instance"
    DEMO_DIR = "demo"
    if not os.path.exists(INSTANCE_DIR):
        os.mkdir(INSTANCE_DIR)
    if not os.path.exists(os.path.join(INSTANCE_DIR, "config.py")):
        shutil.copyfile(os.path.join(DEMO_DIR, "config.py"),
                        os.path.join(INSTANCE_DIR, "config.py"))

    DB_DIR = os.path.join("edustack", "db")
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
    #if not os.path.exists(os.path.join(DB_DIR, "demo.db")):
    if True:
        shutil.copyfile(os.path.join(DEMO_DIR, "demo.db"),
                        os.path.join(DB_DIR, "demo.db"))
    LOGS_DIR = "logs"
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)

    opt_prepare_theme()

def opt_prepare_theme():
    try:
        shutil.rmtree(os.path.join('edustack', 'static'))
        shutil.rmtree(os.path.join('edustack', 'templates'))
    except OSError,e:
        log.warn('rmtree failed, e: %s', e)
    THEMES_DIR = os.path.join("edustack", "themes")
    from config.default import THEME
    shutil.copytree(os.path.join(THEMES_DIR, THEME, 'static'),
                    os.path.join('edustack', 'static'),
                    symlinks=True)
    shutil.copytree(os.path.join(THEMES_DIR, THEME, 'templates'),
                    os.path.join('edustack', 'templates'),
                    symlinks=True)

def _assert_cmd_exist(cmd):
    try:
        subprocess.call(cmd)
    except Exception, e:
        log.warning("{}->{}".format(type(e), e.message))
        log.error("Command '{}' not exist!".format(cmd))
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        showUsage()

    selfModule = __import__(__name__)
    optFunName = "opt_" + sys.argv[1].strip()
    if optFunName not in selfModule.__dict__:
        showUsage()

    if BASE_DIR.strip():
        os.chdir(BASE_DIR)
    selfModule.__dict__[optFunName](*sys.argv[2:])
