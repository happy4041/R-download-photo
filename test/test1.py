#coding=utf-8
import re
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
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
    return imglist
# "http://sabrinacarpenterbr.com/galeria/"
def check1(imglist):
    return 0
        
html = getHtml("http://sabrinacarpenterbr.com/galeria/thumbnails.php?album=1108")

print getImg(html)