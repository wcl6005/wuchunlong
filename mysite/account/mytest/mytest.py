# -*- coding: utf-8 -*-
# 1、新建目录下一定要有__init__.py文件，否则不能被其它文件引用、不能沿路径读写文件。from ... 。
# 2、urls.py中,设置第一级路由名mytest。 在.../mysite/mysite/urls.py中  url(r'^mytest/', include('account.mytest.urls')),
# 3、admin.py中,设置数据库显示。在.../mysite/account/admin.py中 @admin.register(Testusername)
# 4、templates中,增加模板文件目录/mytest
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse,\
    StreamingHttpResponse
from models import Testusername

# http://localhost:8000/mytest/testpost/
def testpost(request):  
    if request.method == 'POST':
        testusers = Testusername(
            username = request.POST['username'],
            password = request.POST['password']
            )
        testusers.save()
        return HttpResponseRedirect('/admin/account/testusername/')
    return  render(request, 'mytest/testpost.html', context=locals()) 
