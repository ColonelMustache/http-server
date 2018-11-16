import socket
import http_helper

to_bind = '0.0.0.0', 80  # tuple of binding info
# start a server socket
server_sock = socket.socket()
server_sock.bind(to_bind)
server_sock.listen(5)  # 5 simultaneous connections (1 handled + 4 in queue)
print 'Running HTTP server on port {0}'.format(to_bind[1])  # to_bind[1] is the port
while True:
    # accept a connection
    client_sock, client_address = server_sock.accept()
    full_request = client_sock.recv(2048)
    # print full_request
    request_http = http_helper.get_request(full_request)
    if request_http:  # request valid
        # print request_http[0]
        data = full_request.split('\r\n\r\n')[1]  # should give me everything after \r\n\r\n, meaning i get all the data
        headers = http_helper.get_headers(full_request)
        # print headers
        http_helper.log_to_file(request_http[0], ", ".join([str(x) for x in client_address]))
        http_helper.handle_request(request_http, client_sock, headers, data)
    else:
        http_helper.bad_request(client_sock)
    client_sock.close()
    print
