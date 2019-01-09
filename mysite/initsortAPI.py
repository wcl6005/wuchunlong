# coding: utf-8 
# 中文排序模块 2017.11.08
# Sorting Chinese Character
import os
import django
import json
# 建立拼音辞典
def dicpy(pyname):
    dic_py = dict()
    f_py = open(pyname,'r')
    content_py = f_py.read()
    lines_py = content_py.split('\n')
    n=len(lines_py)
    for i in range(0,n-1):
        word_py, mean_py = lines_py[i].split('\t', 1)#将line用\t进行分割，最多分一次变成两块，保存到word和mean中去
        dic_py[word_py]=mean_py
    f_py.close()
    return dic_py

# 建立笔画辞典
def dicbh(bhname): 
    dic_bh = dict()
    f_bh = open(bhname,'r')
    content_bh = f_bh.read()
    lines_bh = content_bh.split('\n')
    n=len(lines_bh)
    for i in range(0,n-1):
        word_bh, mean_bh = lines_bh[i].split('\t', 1)#将line用\t进行分割，最多分一次变成两块，保存到word和mean中去
        dic_bh[word_bh]=mean_bh
    f_bh.close()
    return dic_bh 

# 辞典查找函数
def searchdict(dic,uchar):
    if isinstance(uchar, str):
        uchar = unicode(uchar,'utf-8')
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        value=dic.get(uchar.encode('utf-8'))
        if value == None:
            value = '*'
    else:
        value = uchar
    return value
    
#比较单个字符
def comp_char_PY(pyname,bhname,A,B):
    if A==B:
        return -1
    pyA=searchdict(dicpy(pyname),A)
    pyB=searchdict(dicpy(pyname),B)
    if pyA > pyB:
        return 1
    elif pyA < pyB:
        return 0
    else:
        bhA=eval(searchdict(dicbh(bhname),A))
        bhB=eval(searchdict(dicbh(bhname),B))
        if bhA > bhB:
            return 1
        elif bhA < bhB:
            return 0
        else:
            return "Are you kidding?"

#比较字符串
def comp_char(pyname,bhname,charA,charB):
    if isinstance(charA, str):
        charA= unicode(charA,'utf-8')    
    if isinstance(charB, str):
        charB= unicode(charB,'utf-8')    
    
    n=min(len(charA),len(charB))
    i=0
    while i < n:
        dd=comp_char_PY(pyname,bhname,charA[i],charB[i])
        if dd == -1:
            i=i+1
            if i==n:
                dd=len(charA)>len(charB)
        else:
            break
    return dd

# 排序函数
def cn_sort(pyname,bhname,nline):
    n = len(nline)
    lines="\n".join(nline)
    for i in range(1, n):  # 插入法
        tmp = nline[i]
        j = i
        while j > 0 and comp_char(pyname,bhname,nline[j-1],tmp):
            nline[j] = nline[j-1]
            j -= 1
        nline[j] = tmp
    return nline
    
# 调用排序函数,排序结果保存为文件
def cnsort():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission
    from account.models import Material, Order, Company
    pyname = 'mysite/account/sortAPI/py.txt'
    bhname = 'mysite/account/sortAPI/bh.txt'
    namelistpath = 'mysite/account/sortAPI/companynamelist.txt'
    companynamelist = [i['name'] for i in Company.objects.all().values('name')]    
    COMPANY_NAME_LIST = cn_sort(pyname,bhname,companynamelist)
    if not writeJson(namelistpath,COMPANY_NAME_LIST):
        return 'cnsort writeJson err!'      
    for item in COMPANY_NAME_LIST:
        print item
    return 'cnsort ok!'

#保存为json格式文件
def writeJson(filepath,myjson): 
    try:
        fp = open(filepath,'w+')
        fp.write(json.dumps(myjson))
        fp.close() 
        return True
    except Exception,ex:
        return False
if __name__ == '__main__':
    cnsort()    
