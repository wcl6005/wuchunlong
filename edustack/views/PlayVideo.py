#-*- coding: utf-8 -*-

'''
Created on 2016-02-25

@author: Wu Chunlong (wcl6005@126.com)
'''

from flask import Blueprint
from flask import render_template
import json

PlayVideo = Blueprint('PlayVideo', __name__)

#http://localhost:5000/PlayVideo/PlayVideo/
@PlayVideo.route('/AngularJS_Hello/')
def mAngularJS_Hello():
    str='hello world!'
    return render_template(r"PlayVideo/AngularJS_Hello.html",str=str)

@PlayVideo.route('/PlayVideo/')
def mPlayVideo():
	#Playvideos=u'欢迎吴文相光临！'
	Playvideos= u'''{videoname: '/static/PlayVideoFils/video/美女杠铃.mp4' ,img:'/static/PlayVideoFils/img/p1.jpg',playnum:'65',intvideo: '支持全屏播放！2016.3.16'},'''
	return render_template(r"PlayVideo/PlayVideo.html",Playvideos=Playvideos)


