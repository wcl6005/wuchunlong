from flask import render_template as _render_template
from flask import request
from edustack.utils import tryParse

def render_template(*args, **kwargs):
    return _render_template(*args, gt=GTDict, **kwargs)

def _get_page_index():
    pageIndex = request.args.get('page')
    pageIndex = tryParse(pageIndex, int, 1)
    return pageIndex

GTDict = {}

GTDict['layout'] = {}
GTDict['layout']['title'] = 'AbbyTraining'
GTDict['layout']['link_weibo'] = 'http://weibo.com/p/1005052804214754/home'
GTDict['layout']['link_facebook'] = '#'
GTDict['layout']['link_wechat'] = '#'
GTDict['layout']['link_github'] = '#'
GTDict['layout']['link_twitter'] = '#'
GTDict['layout']['link_youtube'] = '#'
GTDict['layout']['powerby_link'] = 'http://abbyDemo.cloudapp.net'
GTDict['layout']['powerby_name'] = 'AbbyTraining'
GTDict['layout']['rights_link'] = 'http://abbyDemo.cloudapp.net'
GTDict['layout']['rights_name'] = 'AbbyTraining'
GTDict['layout']['manage_link'] = '/manage/'
GTDict['layout']['manage_name'] = 'Manage'
GTDict['layout']['footer_ext_links'] = [
    ('weibo', 'http://weibo.com/p/1005052804214754/home'),
    ('facebook', '/'),
    ('wechat', '/'),
    ('github', '/'),
    ('twitter', '/'),
    ('youtube', '/')]
GTDict['layout']['right_ext_links'] = [
    ('Programming', 'http://abbyDemo.cloudapp.net'),
    ('Reading', 'http://abbyDemo.cloudapp.net'),]