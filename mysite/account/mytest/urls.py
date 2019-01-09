# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import mytest

urlpatterns = [
    url(r'^testpost/', mytest.testpost, name="testpost"), #   
      
]