# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import time
import urllib2
import re
import os

#继承 QThread 类
class BigWorkThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    
    #声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(list)
    def __init__(self,url,addr, parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.url = url
        self.addr = addr
    
    # 获取网页html源码    
    def getHtml(self,url):
        proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
        opener = urllib2.build_opener(proxy_handler)
        page = opener.open(url)
        html = page.read()
        return html
    
    # 下载图片
    def getImg(self,html):
        reg = r'src="(.+?\.jpg)" class="image thumbnail"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
    
        for i in range(len(imglist)):
            imglist[i] = "http://sabrinacarpenterbr.com/galeria/"+str(imglist[i])
            imglist[i] = imglist[i].replace('thumb_','')
            i += 1
        self.download(imglist)
    
    def download(self,imglist):
        x = 1
        for imgurl in imglist:
            os.chdir(str(self.addr))
            proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
            opener = urllib2.build_opener(proxy_handler)
            f = opener.open(imgurl)
            data = f.read()
            with open(str(x)+'.jpg','wb') as code:
                code.write(data)
            #urllib.urlretrieve(imgurl,'%s.jpg' % x)
            x+=1
    
    
    
        
    #重写 run() 函数，在里面干大事。
    def run(self):
        #大事
        print 1
        #获取html网页源码
        html = self.getHtml(str(self.url))
        # 打印并执行下载操作
        print self.getImg(html)
        #大事干完了，发送一个信号告诉主线程窗口
        self.finishSignal.emit(['hello,','Done!','!'])
        