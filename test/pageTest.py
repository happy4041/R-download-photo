#coding=utf-8
'''
Created on 2017年7月26日

@author: happy
'''
import urllib2
import re

globalurl = ""
x = 1
def getHtml(url):
    proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
    opener = urllib2.build_opener(proxy_handler)
    page = opener.open(url)
    html = page.read()
    checkPage(html)

def toNextPage():
    global globalurl
    global x
    y = x + 1
    print "page="+str(x)
    globalurl = globalurl.replace("page="+str(x), "page="+str(y))
    x = y
    print globalurl
    getHtml(globalurl)

def checkPage(html):
    reg = r'src="(.+?\.jpg)" class="image thumbnail"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    print imglist
    if len(imglist):
        # list非空
        toNextPage()
    else:
        # list空
        print "一共有"+str(x-1)+"页，程序执行完毕"
        return 0

def countAllPhoto(self,html):
    reg = r'src="(.+?\.jpg)" class="image thumbnail"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    
    return 0

if __name__ == '__main__':
    globalurl = "http://sabrinacarpenterbr.com/galeria/thumbnails.php?album=1107"
    globalurl += "&page=1"
    getHtml(globalurl)
    pass