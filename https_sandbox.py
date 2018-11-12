import socket

my_sock = socket.socket()
my_sock.connect(('www.google.com', 80))

my_sock.send('GET / HTTP/1.1')
print my_sock.recv(4096)
