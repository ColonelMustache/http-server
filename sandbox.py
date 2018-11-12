import re
from datetime import datetime
import http_helper
import sys
import os
# from certbot import
full_running_dir = os.path.dirname(os.path.realpath(__file__)) + '\\'

with open('NotFound.html', 'r+') as stuff:
    stuff.seek(0, 2)
    print stuff.tell()


search_object = re.search('.*(\.\w*)', 'hello.hi.sup.jpg')
print search_object.group(), search_object.group(1)

# search_object = re.search('(.*[^"]\S*[^"])', '"Users\Itay Feldman\Documents\Custom Office Templates\\"
# D:\Documents\Python\Python_2\Projects\http\http_server\\')
# (".*") (^(?!").*^(?!"))
# print search_object.group(), search_object.group(1)#, search_object.group(2)

request = """
GET / HTTP/1.1\r\n
Host: localhost\r\n
Connection: keep-alive\r\n
Cache-Control: max-age=0\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 """ + \
    """
Safari/537.36\r\n
DNT: 1\r\n
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n
Accept-Encoding: gzip, deflate, br\r\n
Accept-Language: he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7\r\n\r\n"""
search_object = re.search('([\S\s]*?)\r\n\r\n', request)
if search_object:
    print ", ".join(x.replace('\n', '') for x in search_object.group(1).split('\r\n'))
    # print 'request = ' + search_object.group(1)
    # print 'resource = ' + search_object.group(2)
    # print 'HTTP version = ' + search_object.group(3)
else:
    print 'None'

# print "'" + search_object.group(2) + "'"

print datetime.now().date()
client_address = 1
print

# with open('index.html', 'r+') as index_html:
#    client_sock.sendall(index_html.read())

handler_dict = {
    'GET': http_helper.handle_get
}

print os.path.dirname(sys.argv[0])

s = '/'
s2 = s.strip('/')
if not s2:
    print 'empty str is false'

print os.stat("NotFound.html").st_size

print sys.argv[0]  # , sys.argv[1]


print os.path.dirname(os.path.realpath(__file__))

"""
On pycharm:
('127.0.0.1', 50210) - [2018-11-04 17:34:55] "GET / HTTP/1.1"
('127.0.0.1', 50211) - [2018-11-04 17:34:55] "GET /css/doremon.css HTTP/1.1"
('127.0.0.1', 50215) - [2018-11-04 17:34:55] "GET /js/jquery.min.js HTTP/1.1"
('127.0.0.1', 50216) - [2018-11-04 17:34:55] "GET /js/box.js HTTP/1.1"
('127.0.0.1', 50217) - [2018-11-04 17:34:55] "GET /js/submit.js HTTP/1.1"
('127.0.0.1', 50218) - [2018-11-04 17:34:55] "GET /imgs/abstract.jpg HTTP/1.1"
('127.0.0.1', 50221) - [2018-11-04 17:34:56] "GET /imgs/favicon.ico HTTP/1.1"

On cmd:
('127.0.0.1', 50152) - [2018-11-04 17:30:51] "GET / HTTP/1.1"
('127.0.0.1', 50153) - [2018-11-04 17:30:51] "GET /css/doremon.css HTTP/1.1"
('127.0.0.1', 50157) - [2018-11-04 17:30:51] "GET /js/jquery.min.js HTTP/1.1"
('127.0.0.1', 50158) - [2018-11-04 17:30:51] "GET /js/box.js HTTP/1.1"
('127.0.0.1', 50159) - [2018-11-04 17:30:51] "GET /js/submit.js HTTP/1.1"
('127.0.0.1', 50160) - [2018-11-04 17:30:51] "GET /imgs/abstract.jpg HTTP/1.1"
('127.0.0.1', 50163) - [2018-11-04 17:30:51] "GET /imgs/favicon.ico HTTP/1.1"
"""

# with open(sys.argv[1]) as args:
# print args.read()

print os.path.exists(full_running_dir + "imgs/favicon.ico")
