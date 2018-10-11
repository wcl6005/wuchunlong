# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from myAPI import checkcode
from . import home

from rest_framework import routers

# http://127.0.0.1:8000/home/users/
router = routers.DefaultRouter()
router.register(r'users', home.UserViewSet)
router.register(r'groups', home.GroupViewSet)

urlpatterns = [    
    url(r'^checkcodeGIF/', checkcode.checkcodeGIF, name="checkcodeGIF"),
    url(r'^getcheckcode/', checkcode.getcheckcode, name="getcheckcode"),
    url(r'^register/', home.register, name="register"),    
    url(r'^login/', home.login, name="login"),
    url(r'^user_list/', home.user_list, name="user_list"),


    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]