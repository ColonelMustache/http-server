import socket
from datetime import datetime

client_sock = socket.socket()
client_address = ("127.0.0.1", 5555)
http_response = \
        """\
    HTTP/1.1 200 OK

    Hello, World!
    """
request = ""
request_http = ['GET', '/', '1.1']
if 'favicon' in request:
    with open('favicon.ico', 'rb+') as favi_file:
        client_sock.sendall(favi_file.read())
else:
    with open('index.html', 'r+') as html_file:
        client_sock.sendall(html_file.read())
client_sock.close()

log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
log_msg = str(client_address) + ' - [%s] \"%s\"\n' % (log_time, request_http[0].strip('\r\n'))
# print log_msg
# log_file.write(log_msg)

# client_sock.send("HTTP/1.1 404 Not Found\r\n"
# "Content-Length: %d\r\n"
# "Content-Type: text/html; charset=UTF-8\r\n"
# "\r\n" % os.stat("NotFound.html").st_size)
