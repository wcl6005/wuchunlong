# -*- coding: utf-8 -*-支持中文
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'myhtml.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/register/$', 'blog.views.register'),
    url(r'^blog/signin/$', 'blog.views.signin'),

    url(r'^blog/index/$', 'blog.views.index'),

    url(r'^blog/PlayVideoOady/$', 'blog.views.PlayVideoOady'),

    url(r'^blog/CreateFile/$', 'blog.views.CreateFile'),


    url(r'^blog/Newtable/$', 'blog.views.Newtable'),
    url(r'^blog/NewtableLessonListFnames/$', 'blog.views.NewtableLessonListFnames'),
    url(r'^blog/gethttp/$', 'blog.views.gethttp'),
    url(r'^blog/basetest/$', 'blog.views.basetest'),
    url(r'^blog/SubmittedQuestions/$', 'blog.views.SubmittedQuestions'),
    url(r'^blog/TechnologyAsk/$', 'blog.views.TechnologyAsk'),
    url(r'^blog/question/$', 'blog.views.question'),
]
