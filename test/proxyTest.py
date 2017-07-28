#coding=utf-8
import urllib2

proxy_handler = urllib2.ProxyHandler({'http': '127.0.0.1:11211'})
opener = urllib2.build_opener(proxy_handler)
r = opener.open('http://httpbin.org/ip')
print r.read()