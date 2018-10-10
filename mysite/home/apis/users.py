# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login 

def registerapi(request):
    if request.method != 'POST':
        mylist = list(User.objects.values())
        return  JsonResponse(mylist,safe=False)      
    cleanData = request.POST.dict()
    username = cleanData.get('name', '')
    isname = User.objects.filter(username = username)
    if isname:  
        msgdict = {'msg': username + ' Username is already in name.'}
        return JsonResponse(msgdict)      
    user = User.objects.create_superuser(username, cleanData.get('email', ''),\
                                          cleanData.get('password', ''))
    user.save()
    auth_login(request, user) 
    return  JsonResponse({})
 
def loginapi(request):   
    if request.method != 'POST':
        mylist = list(User.objects.values())
        return  JsonResponse(mylist,safe=False)      
    cleanData = request.POST.dict()

    user = authenticate(username=cleanData.get('name', ''), \
                        password=cleanData.get('password', '')) 
    if user:
        auth_login(request, user)
        return  JsonResponse({})      
    msgdict = {'msg':'user authenticate err!'}
    return JsonResponse(msgdict) 