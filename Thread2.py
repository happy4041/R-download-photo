# coding: utf-8

from PyQt4 import QtCore, QtGui
from nt import chdir
import time
import urllib2
import re
import os

#继承 QThread 类
class BigWorkThread(QtCore.QThread):
    """docstring for BigWorkThread"""
    
    # 页数是  x-1 页
    x = 1
    # 图片数
    jpgx = 1
    # 专辑内所有图片数
    cPhoto = 0
    # 此时下载的专辑地址
    
    
    #声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(list)
    progress = QtCore.pyqtSignal(list)
    
    
    def __init__(self,url,addr, parent=None):
        super(BigWorkThread, self).__init__(parent)
        self.globalurl = url
        self.addr = addr.replace('\\','/')
        
    # 获取网页html源码    
    def getHtml(self,globalurl):
        proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
        opener = urllib2.build_opener(proxy_handler)
        page = opener.open(str(globalurl))
        html = page.read()
        print "gethtml"
        return html
    
    # 下载图片
    def getImg(self,html):
        reg = r'src="(.+?\.jpg)" class="image thumbnail"'
        imgre = re.compile(reg)
        imglist = re.findall(imgre,html)
        
        domain = self.getDomainTop()
        
        # 图片地址加头
        for i in range(len(imglist)):
            imglist[i] = domain+str(imglist[i])
            imglist[i] = imglist[i].replace('thumb_','')
            i += 1
        #self.download(imglist)
        print "getImg"
        return imglist


    def download(self,imglist):
        for imgurl in imglist:
            
            print "正在下载第"+str(self.jpgx)+"图片"
            #传回进度信号
            self.progress.emit([self.jpgx,self.cPhoto,self.x])
            #print str(self.addr)
            
            #中文地址加编码utf-8
            path = unicode(self.addr , "utf8")
            
            chdir(str(path))
            proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
            opener = urllib2.build_opener(proxy_handler)
            f = opener.open(imgurl)
            data = f.read()
            with open(str(self.jpgx)+'.jpg','wb') as code:
                code.write(data)
            #urllib.urlretrieve(imgurl,'%s.jpg' % x)
            self.jpgx += 1
        print "download"
        #self.toNextPage()

    # 改地址下一页
    def toNextPage(self):
        y = self.x + 1
        globalurl = self.globalurl.replace("page="+str(self.x), "page="+str(y))
        print globalurl
        self.x = y
        print globalurl+"toNextPage"
        #self.getHtml(globalurl)
    
    def countAllPhoto(self):
        cPhoto = 0
        while True:
            html = self.getHtml(self.globalurl)
            imglist = self.getImg(html)
            if len(imglist):
                cPhoto += len(imglist)
                self.toNextPage()
                #self.page += 1
            else:
                # 还原地址
                self.globalurl = self.globalurl.replace("&"+str(cPhoto),"")
                break
        print "图片共"+str(cPhoto)+"张"
        # 还原x
        self.x = 1
        
        print "countAllPhoto"
        #页数
        #self.page = self.page - 1
        return cPhoto


    def runOnePhotoAlbum(self):
        # 加地址尾
        self.globalurl += "&page=1"
        print self.globalurl
        self.cPhoto = self.countAllPhoto()
        self.globalurl += "&page=1"
        while True:
            print 1
            imglist = self.getImg(self.getHtml(self.globalurl))
            #判断是否为空
            if len(imglist):
                self.download(imglist)
                self.toNextPage()
            else:
                print "下载已完成，共"+str(self.jpgx-1)+"张图片"
                break
        
        
    #返回子线程进度方法
    def returnProgress(self):
        self.progress.emit([self.jpgx,self.cPhoto,self.x])
    
    def getDomainTop(self):
        num = str(self.globalurl).find('thumbnails')
        a = str(self.globalurl[0:num])
        return a
    
    #重写 run() 函数，在里面干大事。
    def run(self):
        #大事
        print "开始下载工作"
        #开始下载工作,下载一个专辑里的图片
        self.runOnePhotoAlbum()
        #大事干完了，发送一个信号告诉主线程窗口
        self.finishSignal.emit(['完','成','!'])
        