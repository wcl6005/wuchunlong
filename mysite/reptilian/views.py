# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse
from bs4 import BeautifulSoup 
import re,requests 

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}

def parseUrl(url):
    requests.packages.urllib3.disable_warnings() 
    text=requests.get(url,headers=headers).text   
    return BeautifulSoup(text, 'lxml') 

#拼音 http://localhost:8000/chineseyabla
def chineseyabla(request):
    url = "https://chinese.yabla.com/chinese-pinyin-chart.php"
    try:
        soup = str(parseUrl(url)) #获得网页文本        
        head = '<head>' + re.findall("[<]head[>](.*)[</]head[>]",soup,re.S)[0] + '/head>'
        head = head.replace('"/js/','"https://yabla.vo.llnwd.net/media.yabla.com/js/')        
        head = head.replace('<title>Mandarin Chinese Pinyin Chart with Audio - Yabla Chinese</title>','<title>Mandarin Chinese Pinyin Chart with Audio - 鑫相科技</title>')        
        table = '<table ' + re.findall("[<]table(.*)[</]table[>]",soup,re.S)[0] + '/table>'
        html = '<!DOCTYPE html><html lang="en"><body><div style="padding-left:500px;color:#3ACC3A;font-size:20px;">鑫相科技 - 没有爬不到的数据!</div>'+head+table+'</body></html>'
        print('head+table =',html)
        return HttpResponse(html) 
    except Exception as ex:
        return HttpResponse(str(ex)) 