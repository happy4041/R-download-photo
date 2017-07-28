#coding=utf-8
import urllib
import urllib2
import re

def getHtml(url):
    proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
    opener = urllib2.build_opener(proxy_handler)
    page = opener.open(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)" class="image thumbnail"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    # 加头地址 替换地址为高清图
    for i in range(len(imglist)):
        imglist[i] = "http://sabrinacarpenterbr.com/galeria/"+str(imglist[i])
        imglist[i] = imglist[i].replace('thumb_','')
        i += 1
    x = 1
    for imgurl in imglist:
        urllib.urlretrieve(imgurl,'%s.jpg' % x)
        x+=1


html = getHtml("http://sabrinacarpenterbr.com/galeria/thumbnails.php?album=1108")

print getImg(html)



