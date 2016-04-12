# -*- coding: utf-8 -*-支持中文
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from blog.models import User
from blog.models import Playvideo
import json
import codecs
import copy
#加密
import hashlib
#>>>import hashlib
#>>> hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
#'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'

#登录。  登录成功，username传递给了index.html，render_to_response('index.html',{'username':username.encode('utf-8')})
#因index.html与base.html之间采用了双向数据梆定，username传递给了index.html后，index.html向base.html传递了username
#详见：云笔记：AngularJS资料 django模板包含基础模板，AngulerJS同时都使用函数的方法(太有用了,不能删除)
#吴春龙 2016.4.10
def signin(request):
    #获得表单用户名
    username= request.GET.get('username','')
    #获得密码
    password= request.GET.get('password','')
    #获得加密密码
    password=hashlib.sha224(password).hexdigest()
    if username:
        strusername=User.objects.all()
        for str in strusername:
            #获得数据库中与用户名相对应的加密密码passwdusername
            if(username==str.username):
                passwdusername=str.password
                # 判断输入的密码与数据库中的密码是否相等
                if password == passwdusername:
                    #return HttpResponse('登录成功！'+username.encode('utf-8'))
                    username=username.encode('utf-8')
                    return render_to_response('searchoday.html',{'username':username})
                    #return  HttpResponse('注册成功！')
    q=request.GET.get('q','')
    username=request.GET.get('username','')
    if q:
        return render_to_response('searchoday.html',{'q':q,'username':username})

    return render_to_response('signin.html',{})

#注册 http://localhost:8000/blog/register/
#用户名唯一，不重复，密码加密后，写入数据库
def register(request):
    #获得用户名
    username= request.GET.get('username','')

    #获得密码
    password= request.GET.get('password','')
    #获得验证码
    checkcode= request.GET.get('checkcode','')
    if username:

    #获得数据库中用户名对象
        usernames=User.objects.all().filter(username=username)
        for str1 in usernames:
            if username == str1.username:
                #支持中文
                strusername=username+u'用户已经存在,请重新注册！'

                return render_to_response('register.html',{'strusername':strusername})
        #获得密码密文passwdusername
        passwdusername=hashlib.sha224(password).hexdigest()

        #写入数据库   添加数据库记录
        user = User()
        user.username = username
        user.password = passwdusername
        user.checkcode = checkcode
        user.save()
        return  HttpResponse('注册成功！admin查看！')
        #return render_to_response('signin.html',{'username':username,'password':password,'checkcode':checkcode, })
    return render_to_response('register.html',{})

def PlayVideoOady(request):
    #播放
    filename = request.GET.get('filename','')
    id = request.GET.get('id','')
    if filename:
        fname=filename[35:-4]
        #return  HttpResponse('classification')
        return render_to_response('PlayVideoOady.html',{'filename':filename,'fname':fname,'id':id,})
    #搜索
    q=request.GET.get('q','')
    if q:
        return render_to_response('searchoday.html',{'q':q,})
    return render_to_response('PlayVideoOady.html',{})


#从数据库中读取数据，保存为/static/oday/php/dbfile.php文件
def CreateFile(request):
    PlayvideoList=[]
    #获得从数据库中获得视频文件对象
    Playvideos=Playvideo.objects.all()
    for mPlayvideo in Playvideos:
        intvideodata=mPlayvideo.intvideo.encode('utf-8')#转为Unicode
        playnumdata=mPlayvideo.playnum.encode('utf-8')#转为Unicode
        aPlayvideo='{'+'"'+'videoname'+'"'+':'+'"'+'/'+str(mPlayvideo.videoname) +'"'+ ','+'"'+'img'+'"'+':'+'"'+'/'+ str(mPlayvideo.img)+'"'+ ','+'"'+'playnum'+'"'+':'+'"'  +playnumdata+'"' + ','+'"'+'intvideo'+'"'+':'+'"'+intvideodata+'"' +' },'
        PlayvideoList.append(aPlayvideo)#将所有视频信息添加到列表中
    #所有视频信息转换成字符串:
    Playvideos='{'+ '"records"'+':[' + ''.join(PlayvideoList)
    Playvideos=Playvideos[0:-1]+']'+'}'

    #如果文件不存在，则自动创建文件;如果文件存在,清零
    file_object = codecs.open('./static/oday/php/dbfile.php', 'w')
    file_object.close()
    file_object = codecs.open('./static/oday/php/dbfile.php', 'r+')

    file_object.write(Playvideos)
    file_object.close()
    return HttpResponse(Playvideos)


def gethttp(request):
    return render_to_response('gethttp.html',{})

def index(request):
    q=request.GET.get('q','')
    if q:
        return render_to_response('searchoday.html',{'q':q,'searchoday':'searchoday.html'})
        #return HttpResponse(q)
    return render_to_response('index.html',{})

#django模板 可以使用AngularJS ng-include 指令来包含 HTML 内容 勿删   吴春龙 2016.4.8
def basetest(request):
    q=request.GET.get('q','')
    if q:
        return render_to_response('searchoday.html',{'q':q,})
    return render_to_response('basetest.html',)



#1、从Newtable.html，获得PlayLessons、PlayLessonLists
#2、创建新表dbfile.php,保存在/static/oday/php/dbfile.php
#3、http://localhost:8000/blog/Newtable/  调用网页Newtable.html 勿删   吴春龙 2016.4.1
def Newtable(request):
    PlayLessons = request.GET.get('PlayLessons','')
    PlayLessonLists= request.GET.get('PlayLessonLists','')
    if PlayLessons:
        PlayLessons=json.loads(PlayLessons)
        PlayLessonLists=json.loads(PlayLessonLists)
        listPlayLesson=[]
        for PlayLesson in PlayLessons:
            PlayLesson_id=int(PlayLesson["id"])
            dictPlayLesson={}
            n=1
            numbersum=0
            timesum=0
            #字典拷贝
            dictPlayLesson=PlayLesson.copy()
            for PlayLessonList in PlayLessonLists:
                PlayLessonList_id=int(PlayLessonList["id"])
                if PlayLesson_id==PlayLessonList_id:
                    #添加到字典
                    numbering=PlayLessonList["numbering"]
                    filename=PlayLessonList["filename"]
                    fname=filename[35:-4]
                    description=PlayLessonList["description"]
                    time=PlayLessonList["time"]
                    number=PlayLessonList["number"]
                    date=PlayLessonList["date"]


                    dictPlayLesson["numbering"+str(n)]=numbering
                    dictPlayLesson["filename"+str(n)]=filename
                    dictPlayLesson["fname"+str(n)]=fname
                    dictPlayLesson["description"+str(n)]=description
                    dictPlayLesson["time"+str(n)]=time
                    dictPlayLesson["number"+str(n)]=number
                    dictPlayLesson["date"+str(n)]=date
                    n=n+1
                    timesum=timesum+int(time)
                    numbersum=numbersum+int(number)
                    dictPlayLesson["id"]=int(PlayLesson_id)
            dictPlayLesson["numbersum"]=numbersum
            dictPlayLesson["lessonssum"]=n-1
            dictPlayLesson["timesum"]=timesum
            #添加到列表
            listPlayLesson.append(dictPlayLesson)

        #显示中文,没有下列语句不能显示中文
        listPlayLesson=json.dumps(listPlayLesson, ensure_ascii=False)
        listPlayLesson='{'+ '"records":'+listPlayLesson.encode('utf-8')+"}"

        #如果文件不存在，则自动创建文件;如果文件存在,清零
        file_object = open('./static/oday/php/dbfile.php', 'w')
        file_object.close()
        file_object = codecs.open('./static/oday/php/dbfile.php', 'r+')

        file_object.write(listPlayLesson)
        file_object.close()

        #return HttpResponse(listPlayLesson)
        return HttpResponse("./static/oday/php/dbfile.php,  创建新表成功！</br>"+listPlayLesson)

    return render_to_response('Newtable.html',{})


#PlayLessonLists.php添加短文件名fname到列表（列表元素是字典）,创建新表,保存在/static/oday/php/NewtableLessonListFnames.php
#勿删  吴春龙 2016.4.5
def NewtableLessonListFnames(request):
    PlayLessonLists= request.GET.get('PlayLessonLists','')
    if PlayLessonLists:
        PlayLessonLists=json.loads(PlayLessonLists)
        for PlayLessonList in PlayLessonLists:
            #添加到字典
            filename=PlayLessonList["filename"]
            fname=filename[35:-4]
            PlayLessonList["fname"]=fname

        #显示中文,没有下列语句不能显示中文
        listPlayLesson=json.dumps(PlayLessonLists, ensure_ascii=False)
        listPlayLesson='{'+ '"records":'+listPlayLesson.encode('utf-8')+"}"

        #如果文件不存在，则自动创建文件;如果文件存在,清零
        file_object = open('./static/oday/php/NewtableLessonListFnames.php', 'w')
        file_object.close()
        file_object = codecs.open('./static/oday/php/NewtableLessonListFnames.php', 'r+')

        file_object.write(listPlayLesson)
        file_object.close()

        return HttpResponse("./static/oday/php/NewtableLessonListFnames.php,  创建新表成功！</br>"+listPlayLesson)
    return render_to_response('NewtableLessonListFnames.html',{})



#两表合一,创建新表,增加课总数、总人数、课时总数 ,保存在/static/oday/php/dbfile.php
# 勿删  吴春龙 2016.4.4
#def Newtable(request):  #测试
def Newtable3(request):
    PlayLessons = request.GET.get('PlayLessons','')
    PlayLessonLists= request.GET.get('PlayLessonLists','')
    #增加课总数、总人数、课时总数
    if PlayLessons:
        PlayLessons=json.loads(PlayLessons)
        PlayLessonLists=json.loads(PlayLessonLists)
        for PlayLesson in PlayLessons:
            PlayLessonID=int(PlayLesson['id'])
            #课总数
            lessonssumMAX=0
            #总人数
            numbersum=0
            #课时总数
            timesum=0
            for PlayLessonList in PlayLessonLists:
                PlayLessonListID=int(PlayLessonList['id'])
                if PlayLessonID==PlayLessonListID:
                    lessonssumMAX+=1
                    numbersum+=int(PlayLessonList['number'])
                    timesum+=int(PlayLessonList['time'])

            #写入字典
            for PlayLessonList in PlayLessonLists:
                PlayLessonListID=int(PlayLessonList['id'])
                if PlayLessonID==PlayLessonListID:
                    PlayLessonList['lessonssum']=str(lessonssumMAX)
                    PlayLessonList['numbersum']=str(numbersum)
                    PlayLessonList['timesum']=str(timesum)
        #显示中文,没有下列语句不能显示中文
        #PlayLessonLists=json.dumps(PlayLessonLists, ensure_ascii=False)
        #return HttpResponse(PlayLessonLists)
    #return render_to_response('Newtable.html',{})

    #两表合一
    if PlayLessons:
        #PlayLessons=json.loads(PlayLessons)
        #PlayLessonLists=json.loads(PlayLessonLists)
        mystr=""
        for PlayLesson in PlayLessons:
            PlayLessonID=int(PlayLesson['id'])
            PlayLesson=json.dumps(PlayLesson, ensure_ascii=False)
            PlayLesson=PlayLesson[:-1]+','
            for PlayLessonList in PlayLessonLists:
                PlayLessonListID=int(PlayLessonList['id'])
                if PlayLessonListID==PlayLessonID:
                    #获得文件名
                    filename=PlayLessonList['filename']
                    filename=json.dumps(filename, ensure_ascii=False)
                    fname=filename[36:-5]
                    #增加短文件名 写入字典
                    PlayLessonList['fname']=fname
                    #拷贝 字典
                    PlayLessonListDACT=PlayLessonList.copy()
                    #删除 字典元素id
                    PlayLessonListDACT.pop('id')

                    PlayLessonList=json.dumps(PlayLessonListDACT, ensure_ascii=False)
                    PlayLessonList=PlayLessonList[1:]

                    mystr=mystr+PlayLesson+PlayLessonList+','
        mystr=mystr[:-1]
        listPlayLesson='{'+ '"records":['+mystr.encode('utf-8')+"]}"

        #如果文件不存在，则自动创建文件;如果文件存在,清零
        file_object = open('./static/oday/php/dbfile.php', 'w')
        file_object.close()
        file_object = codecs.open('./static/oday/php/dbfile.php', 'r+')

        file_object.write(listPlayLesson)
        file_object.close()

        return HttpResponse(listPlayLesson)
    return render_to_response('Newtable.html',{})

#进入播放页后 提问 提交问题
def SubmittedQuestions(request):
    #问题标题
    qa_sub_title = request.GET.get('qa_sub_title','')
    #有新回答时请邮件提醒我
    send_email = request.GET.get('send_email','')
    #"1"-- 十万火急 "2"-- 着急，拜托快点  "3"-- 不急，慢慢解决
    qalevel = request.GET.get('qalevel','')
    #问题内容
    editor= request.GET.get('editor','')
    if qa_sub_title:
        return HttpResponse( qa_sub_title+"----"+send_email+"----"+qalevel+"---"+editor)

    q=request.GET.get('q','')
    if q:
        return render_to_response('searchoday.html',{'q':q,})
        #return HttpResponse(q)
    return render_to_response('index.html',)

#首页 技术问答
def TechnologyAsk(request):
    q=request.GET.get('q','')
    if q:
        return render_to_response('searchoday.html',{'q':q,})
    return render_to_response('TechnologyAsk.html',{})

def question(request):
    editor= request.GET.get('editor','')
    if editor:
        return HttpResponse(editor)
    return render_to_response('question.html',{})





