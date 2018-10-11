# -*- coding: utf-8 -*-
from django.shortcuts import render
from myAPI.checkcode import gcheckcode
   
def login(request):   
    return  render(request, 'home/login.html' , context=locals()) 

def register(request):
    g_checkcode = gcheckcode(request)#验证码送前台验证
    print('g_checkcode =',g_checkcode)
    return  render(request, 'home/register.html' , context=locals()) 

# http://127.0.0.1:8000/home/user_list/
def user_list(request):   
    return  render(request, 'home/user_list.html' , context=locals()) 

#---------------------------Django-Rest-Framework框架----------------------------#
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer