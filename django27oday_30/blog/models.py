# -*- coding: utf-8 -*-支持中文
from django.db import models
# Create your models here.
from django.contrib import admin

#用户数据模型
class User(models.Model):
    #用户名
    username = models.CharField(max_length = 30)
    #密码
    password = models.CharField(max_length = 80)
    #验证码
    checkcode = models.CharField(max_length = 30)

    def __str__(self):
        return self.username
    def __str__(self):
        return self.password
    def __str__(self):
        return self.checkcode

#播放数据模型
#videoname视频文件  img缩位图  playnum播放次数   intvideo视频简介
class Playvideo(models.Model):
    videoname = models.FileField(upload_to = './static/angularjsfile/video/')#创建该目录,存放上传的视频文件
    img = models.FileField(upload_to = './static/angularjsfile/img/') #创建该目录,存放上传的缩位图
    playnum = models.CharField(max_length = 30)
    intvideo = models.CharField(max_length = 30)
    def __str__(self):
        return self.videoname
    def __str__(self):
        return self.img
    def __str__(self):
        return self.playnum
    def __str__(self):
        return self.intvideo

#Admin必须用 list_display
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('username','password','checkcode')


#Admin必须用 list_display
class PlayvideoAdmin(admin.ModelAdmin):
    list_display = ('videoname','img','intvideo')


#注册
admin.site.register(User,BlogPostAdmin)
admin.site.register(Playvideo,PlayvideoAdmin)