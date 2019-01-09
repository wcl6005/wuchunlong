# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#本框架 数据库名称不能用User，否则出错！
#from django.contrib.auth.models import User
from django.db import models

class Testusername(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, unique=True)     
    def __unicode__(self):
        return self.name
    