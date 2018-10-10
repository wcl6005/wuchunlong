# -*- coding: utf-8 -*-
from django.shortcuts import render
from myAPI.checkcode import gcheckcode
   
def login(request):   
    return  render(request, 'home/login.html' , context=locals()) 

def register(request):
    g_checkcode = gcheckcode(request)#验证码送前台验证
    return  render(request, 'home/register.html' , context=locals()) 
