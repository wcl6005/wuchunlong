'''
Created on 2016-04-12

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

import markdown2
from flask_restful import abort
from flask_login import login_required, current_user
from edustack.models.blog import Blog, Comment
from edustack.models import toDict, get_items_by_page, db
from edustack.apis import addArg, ApiBase, api_res, ArgPage, ArgFormat
from flask_restful.reqparse import Argument


ArgBlogName = Argument('name', required=True, trim=True, help='Invalid name')
ArgBlogSummary = Argument('summary', required=True, trim=True, help='Invalid summary')
ArgBlogContent = Argument('content', required=True, trim=True, help='Invalid content')

@addArg(getBlog=[ArgPage, ArgFormat])
@addArg(postBlog=[ArgBlogName, ArgBlogSummary, ArgBlogContent])
class API_Blogs(ApiBase):
    def get(self):
        args = self.getArgs('getBlog')
        _page, _format = args['page'], args['format']

        blogs, page = get_items_by_page(_page, Blog)
        if _format == 'html':
            for blog in blogs:
                blog.content = markdown2.markdown(blog.content)

        return dict(blogs=[toDict(i) for i in blogs], page=page.toDict())

    @login_required
    def post(self):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postBlog')

        if not args['name']:
            abort(400, message="name can not be empty!")
        if not args['summary']:
            abort(400, message="summary can not be empty!")
        if not args['content']:
            abort(400, message="content can not be empty!")

        blog = Blog(current_user.id, args['name'], args['summary'], args['content'])
        db.session.add(blog)
        db.session.commit()
        ret = Blog.query.filter_by(id=blog.id).first()
        return toDict(ret)

@addArg(postBlog=[ArgBlogName, ArgBlogSummary, ArgBlogContent])
class API_Blog(ApiBase):
    def get(self, id):
        blog = Blog.query.filter_by(id=id).first()
        if blog is None:
            abort(404, message="Blog {0} do not exist.".format(id))
        return toDict(blog)

    @login_required
    def delete(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        blog = Blog.query.filter_by(id=id).first()
        if blog is None:
            abort(404, message="Blog {0} do not exist.".format(id))
        db.session.delete(blog)
        db.session.commit()
        return toDict(blog)

    @login_required
    def post(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        args = self.getArgs('postBlog')

        if not args['name']:
            abort(400, message="name can not be empty!")
        if not args['summary']:
            abort(400, message="summary can not be empty!")
        if not args['content']:
            abort(400, message="content can not be empty!")

        blog = Blog.query.filter_by(id=id).first()
        blog.name = args['name']
        blog.summary = args['summary']
        blog.content = args['content']
        db.session.commit()
        blog = Blog.query.filter_by(id=id).first()
        return toDict(blog)

ArgCommentContent = Argument('content', required=True, trim=True, help='Invalid content')

@addArg(postComment=[ArgCommentContent])
class API_Comment(ApiBase):
    def get(self, id):
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            abort(404, message="Comment {0} do not exist.".format(id))
        return toDict(comment)

    @login_required
    def delete(self, id):
        if not current_user.admin:
            abort(403, message="No Permission!")
        comment = Comment.query.filter_by(id=id).first()
        if comment is None:
            abort(404, message="Comment {0} do not exist.".format(id))
        db.session.delete(comment)
        db.session.commit()
        return toDict(comment)

    @login_required
    def post(self, id):
        args = self.getArgs('postComment')
        blog = Blog.query.filter_by(id=id).first()
        if not blog:
            abort(404, message="Blog {0} do not exist.".format(id))

        content = args['content']
        if not content:
            abort(400, message="content can not be empty!")

        comment = Comment(user_id=current_user.id,
                          blog_id=id,
                          content=content)
        db.session.add(comment)
        db.session.commit()
        comment = Comment.query.filter_by(id=comment.id).first()
        return toDict(comment)

@addArg(getComment=[ArgPage, ArgFormat])
class API_Comments(ApiBase):
    def get(self):
        args = self.getArgs('getComment')
        _page, _format = args['page'], args['format']
        comments, page = get_items_by_page(_page, Comment)
        return dict(comments=[toDict(i) for i in comments], page=page.toDict())

api_res.add_resource(API_Blogs, '/blogs')
api_res.add_resource(API_Blog, '/blogs/<md5_id:id>')
api_res.add_resource(API_Comments, '/comments')
api_res.add_resource(API_Comment, '/comments/<md5_id:id>')