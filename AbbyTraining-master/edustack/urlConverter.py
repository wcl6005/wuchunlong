'''
Created on 2016-04-24

@author: Wu Wenxiang (wuwenxiang.sh@gmail.com)
'''

from werkzeug.routing import BaseConverter


class Md5IdConverter(BaseConverter):
    regex = r'[0-9a-z]{50}/?'

ConverterDict = {'md5_id' : Md5IdConverter}