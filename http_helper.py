import re
import os
from datetime import datetime
import csv
full_running_dir = os.path.dirname(os.path.realpath(__file__)) + '\\'
# TODO write DOCSTRING comments for all functions later


def get_request(request):
    search_object = re.search('([A-Z]+) (/.*)+ HTTP/([0-9]\.[0-9])\r\n', request)
    # group1 = request, group2 = resource, group3 = http version
    if search_object:
        # matched query and the 3 groups
        return [search_object.group(), search_object.group(1), search_object.group(2), search_object.group(3)]
    return False


def bad_request(client_sock):
    # print '400 Bad Request'
    # print full_request
    # with open('BadRequest.html', 'r+') as bad_request_html:
        # client_sock.sendall(bad_request_html.read())
    header = "HTTP/1.1 400 Bad Request\r\n"
    client_sock.send(header)


def handle_request(params, client_sock):
    # params = [full request, request type, resource, http version] <=> [0, 1, 2, 3]
    request = params[1]  # i.e GET
    if request == 'GET':
        handle_get(params[2].strip('/'), client_sock)
    elif request == 'POST':
        handle_post()
    else:
        handle_internal_error(client_sock)


# requests handling:
def handle_get(resource, client_sock):
    check_exception(resource, client_sock)
    if not resource and os.path.exists("index.html"):
        # first request of default page
        with open("index.html", 'rb') as index_html:
            header = "HTTP/1.1 200 OK\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: text/html; charset=UTF-8\r\n" \
                     "\r\n".format(len(open('./index.html', 'rb').read()))
            client_sock.send(header)
            client_sock.sendall(index_html.read())
    elif os.path.exists(full_running_dir + resource):
        # send the requested resource
        with open(resource, 'rb+') as requested_resource:
            # print "resource:", resource
            header = "HTTP/1.1 200 OK\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: {1}\r\n" \
                     "\r\n".format(len(open(resource, 'rb').read()), get_content_type(resource))  # str(os.stat(resource).st_size)
            client_sock.send(header)
            client_sock.sendall(requested_resource.read())
    else:
        # 404 page not found
        with open("statusCodes/NotFound.html", 'rb') as not_found_html:
            header = "HTTP/1.1 404 Not Found\r\n" \
                     "Content-Length: {0}" \
                     "Content-Type: text/html; charset=UTF-8\r\n" \
                     "\r\n".format(len(open('statusCodes/NotFound.html', 'rb').read()))

            """There is no Content-Length header because no matter what I do, for some reason, 
            the file the browser receives is smaller than the size I specify which leads
            to an error even though the file *on my computer* is the correct size,
            that's why format is commented out as well"""

            client_sock.send(header)
            client_sock.sendall(not_found_html.read())
    log_to_file(' | '.join(header.strip('\r\n').split('\r\n')), 'localhost, 80')


def handle_post():
    pass


def log_to_file(to_log, address):
    date = datetime.now().date()
    if not os.path.exists("logs"):
        os.mkdir("./logs")
    with open('logs/http_server_{0}.log'.format(date), 'a+') as log_file:
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = str(address) + ' - [%s] \"%s\"\n' % (log_time, to_log.strip('\r\n'))
        # print log_msg
        log_file.write(log_msg)


def get_content_type(file_name):
    search_object = re.search('.*\.(\w*)', file_name)
    file_type = search_object.group(1).upper()
    # print file_type
    if file_type == 'TXT' or file_type == 'HTML':
        content_type = 'text/html; charset=UTF-8'
    elif file_type == 'JPG' or file_type == 'JPEG':
        content_type = 'image/jpeg'
    elif file_type == 'JS':
        content_type = 'text/javascript; charset=UTF-8'
    elif file_type == 'CSS':
        content_type = 'text/css'
    elif file_type == 'GIF':
        content_type = 'image/gif'
    elif file_type == 'ICO':
        content_type = 'image/ico'
    elif file_type == 'PNG':
        content_type = 'image/png'
    else:
        content_type = 'file/unknown'

    return content_type


def check_forbidden(resource):
    # print resource
    if resource == 'exceptions/forbidden.txt':
        return True
    with open('exceptions/forbidden.txt', 'rb+') as forbidden:
        data = forbidden.read().splitlines()
        exception_type = data[0]
        files = data[1:]
        # print files
        if exception_type.upper() == 'WHITELIST':
            if resource in files:
                return False
            return True
        elif exception_type.upper() == "BLACKLIST":
            if resource in files:
                return True
            return False
        else:
            print 'Forbidden list type not configured correctly\n' \
                  'file must start like so: "*type*(whitelist | blacklist):"\n' \
                  'Responding with "not forbidden"'
            return False


def handle_forbidden(client_sock):
    # code gets here if the file requested was forbidden to access
    with open("statusCodes/Forbidden.html", 'rb') as forbidden:
        header = "HTTP/1.1 403 Forbidden\r\n" \
                 "Content-Length: %d\r\n" \
                 "Content-Type: text/html; charset=UTF-8\r\n" \
                 "\r\n" % len(open("statusCodes/Forbidden.html", 'rb').read())
        client_sock.send(header)
        client_sock.sendall(forbidden.read())


def check_moved_temp(resource):
    with open('exceptions/moved_temp.csv', 'rb') as files_dict:
        reader = csv.reader(files_dict)
        moved_dict = {}
        for row in reader:
            moved_dict[row[0]] = row[1]
    try:
        return moved_dict[resource]
    except KeyError:
        return False


def handle_moved_temp(client_sock, new_location):
    # TODO if moved function returns: True, *new_location* = true, resource was moved; *new_location*, the new location
    # TODO if not moved function returns: False, '' = false, not moved; '', empty string so there won't be an IndexError
    header = "HTTP/1.1 302 Moved Temporarily\r\n" \
             "Location: {0}\r\n" \
             "\r\n".format(new_location)
    client_sock.send(header)


def check_exception(resource, client_sock):
    moved_temp = check_moved_temp(resource)
    if check_forbidden(resource):
        handle_forbidden(client_sock)
    elif moved_temp:
        handle_moved_temp(client_sock, moved_temp)


def handle_internal_error(client_sock):
    header = "HTTP/1.1 500 Internal Server Error\r\n" \
             "\r\n"
    client_sock.send(header)
