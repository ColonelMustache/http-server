import re
import os
from datetime import datetime
import csv
full_running_dir = (os.path.dirname(__file__) + '\\').replace('\\', '/')
# TODO write DOCSTRING comments for all functions later


def get_request(request):
    search_object = re.search('([A-Z]+) (/.*)+ HTTP/([0-9]\.[0-9])\r\n', request)
    # group1 = request, group2 = resource, group3 = http version
    if search_object:
        # matched query and the 3 groups
        return [search_object.group(), search_object.group(1), search_object.group(2), search_object.group(3)]
    return False


def get_headers(request):
    headers = ['content_length', 'content_type']
    headers_values = parse_separate_headers(request)
    return dict((headers[i], headers_values[i]) for i in range(0, len(headers_values)))


def parse_separate_headers(request):
    content_length = re.search('Content-Length: (.*)\r\n', request)
    content_type = re.search('Content-Type: (.*)\r\n', request)
    headers_values = [content_length, content_type]
    for i in range(0, len(headers_values)):
        try:
            headers_values[i] = headers_values[i].group(1)
        except AttributeError:
            headers_values[i] = 'empty'
    return headers_values


def bad_request(client_sock):
    header = "HTTP/1.1 400 Bad Request\r\n" \
             "\r\n"
    client_sock.send(header)
    log_to_file(' | '.join(header.strip('\r\n').split('\r\n')), 'localhost, 80')


def handle_request(params, client_sock, headers, extra_data):
    # params = [full request, request type, resource, http version] <=> [0, 1, 2, 3]
    request = params[1]  # i.e GET
    if request == 'GET':
        handle_get(params[2].strip('/'), client_sock)
    elif request == 'POST':
        handle_post(params[2].strip('/'), client_sock, headers, extra_data)
    else:
        handle_internal_error(client_sock)


def handle_others_on_get(resource, client_sock):
    exceptions_header = check_exception(resource, client_sock)
    webpage_functions_header = webpage_functions(resource, client_sock)
    headers_list = [exceptions_header, webpage_functions_header]
    for header in headers_list:
        if header:
            return header
    return False


# requests handling:
def handle_get(resource, client_sock):
    base_header = handle_others_on_get(resource, client_sock)
    if base_header:
        header = base_header
    elif not resource and os.path.exists(full_running_dir + "index.html"):
        # first request of default page
        with open(full_running_dir + "index.html", 'rb') as index_html:
            data = index_html.read()
            header = "HTTP/1.1 200 OK\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: text/html; charset=UTF-8\r\n" \
                     "\r\n".format(len(data))
            client_sock.send(header)
            client_sock.sendall(data)
    elif os.path.exists(full_running_dir + resource):
        # send the requested resource
        with open(full_running_dir + resource, 'rb+') as requested_resource:
            data = requested_resource.read()
            header = "HTTP/1.1 200 OK\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: {1}\r\n" \
                     "\r\n".format(len(data), get_content_type(resource))
            client_sock.send(header)
            client_sock.sendall(data)
    else:
        # 404 page not found
        with open(full_running_dir + "statusCodes/NotFound.html", 'rb') as not_found_html:
            data = not_found_html.read()
            header = "HTTP/1.1 404 Not Found\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: text/html; charset=UTF-8\r\n" \
                     "\r\n".format(len(data))

            """There is no Content-Length header because no matter what I do, for some reason, 
            the file the browser receives is smaller than the size I specify which leads
            to an error even though the file *on my computer* is the correct size,
            that's why format is commented out as well"""

            client_sock.send(header)
            client_sock.sendall(data)
    log_to_file(' | '.join(header.strip('\r\n').split('\r\n')), 'localhost, 80')


def handle_post(request, client_sock, headers, extra_data):
    try:
        content_length = int(headers['content_length'])  # *int!*
    except ValueError:
        # no content length header
        content_length = False
    destination, variables = split_resource(request)
    # print "length:", content_length
    # print content_length, destination, variables, 'HELLO'
    file_contents = extra_data
    if not os.path.exists('upload/'):
        os.mkdir('upload/')
    if check_allowed_upload(destination, variables['file-name']):
        with open(full_running_dir + destination + '/' + variables['file-name'], 'wb+') as new_file:
            if content_length:
                file_contents += get_file_content_from_post(client_sock, content_length - len(extra_data))
            else:
                file_contents += get_file_content_from_post(client_sock, False)
            new_file.write(file_contents)
            header = "HTTP/1.1 201 Created\r\n" \
                     "\r\n"
            client_sock.send(header)
            client_sock.send('Success!')
            log_to_file(' | '.join(header.strip('\r\n').split('\r\n')), 'localhost, 80')


def check_allowed_upload(folder, file_name):
    """
    Checks if a file should be allowed access to. For security reasons.
    :param folder:
    :param file_name:
    :return:
    """
    full_dir = folder + '/' + file_name
    if os.path.isfile(full_running_dir + full_dir):
        if full_dir in open(full_running_dir + 'data/allowedToUploadAndEdit', 'r').read().splitlines():
            return True
        return False
    else:
        if check_is_in_allowed_files(full_dir):
            open(full_running_dir + 'data/allowedToUploadAndEdit', 'a+').write(full_dir + '\n')  # added to legal files
    return True  # if file doesnt exist it is ok


def check_is_in_allowed_files(file_to_check):
    with open(full_running_dir + 'data/allowedToUploadAndEdit', 'a+') as allowed_files:
        allowed_files_list = allowed_files.read().splitlines()
        if file_to_check not in allowed_files_list:
            return True
        return False


def get_file_content_from_post(client_sock, left_data_length):
    data = ''
    if left_data_length:
        while len(data) < left_data_length:
            new_data = client_sock.recv(4096)
            data += new_data
    else:
        while True:
            new_data = client_sock.recv(4096)
            if not new_data:
                break
            data += new_data
    return data  # all of the rest of the data of the file


def log_to_file(to_log, address):
    date = datetime.now().date()
    if not os.path.exists(full_running_dir + "logs"):
        os.mkdir("./logs")
    with open(full_running_dir + 'logs/http_server_{0}.log'.format(date), 'a+') as log_file:
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = str(address) + ' - [%s] \"%s\"\n' % (log_time, to_log.strip('\r\n'))
        log_file.write(log_msg.replace('//', '/'))


def get_content_type(file_name):
    search_object = re.search('.*\.(\w*)', file_name)
    file_type = search_object.group(1).upper()
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
    if resource == 'exceptions/forbidden.txt':
        return True
    with open(full_running_dir + 'exceptions/forbidden.txt', 'rb+') as forbidden:
        data = forbidden.read().splitlines()
        exception_type = data[0]
        files = data[1:]
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


def resource_is_in_forbidden(resource, files):
    for item in files:
        search_object = re.search(item, resource)
        if search_object:
            return True


def handle_forbidden(client_sock):
    # code gets here if the file requested was forbidden to access
    with open(full_running_dir + "statusCodes/Forbidden.html", 'rb') as forbidden:
        data = forbidden.read()
        header = "HTTP/1.1 403 Forbidden\r\n" \
                 "Content-Length: %d\r\n" \
                 "Content-Type: text/html; charset=UTF-8\r\n" \
                 "\r\n" % len(data)
        client_sock.send(header)
        client_sock.sendall(data)
    return header


def check_moved_temp(resource):
    with open(full_running_dir + 'exceptions/moved_temp.csv', 'rb') as files_dict:
        reader = csv.reader(files_dict)
        moved_dict = {}
        for row in reader:
            moved_dict[row[0]] = row[1]
    try:
        return moved_dict[resource]
    except KeyError:
        return False


def handle_moved_temp(client_sock, new_location):
    header = "HTTP/1.1 302 Moved Temporarily\r\n" \
             "Location: {0}\r\n" \
             "\r\n".format(new_location)
    client_sock.send(header)
    return header


def check_exception(resource, client_sock):
    moved_temp = check_moved_temp(resource)
    if check_forbidden(resource):
        return handle_forbidden(client_sock)
    elif moved_temp:
        return handle_moved_temp(client_sock, moved_temp)
    return False


def handle_internal_error(client_sock):
    header = "HTTP/1.1 500 Internal Server Error\r\n" \
             "\r\n"
    client_sock.send(header)


def webpage_functions(resource, client_sock):
    if '?' not in resource:
        return False
    method_name, variables = split_resource(resource)
    method = check_functions(method_name)
    if method[0]:
        header = method[1](variables, client_sock)
        return header
    return False
    # if no method exists return nothing and continue main program, will either get a resource or a 404


def check_functions(resource):
    with open(full_running_dir + 'data/siteFuncs', 'r+') as fh:
        funcs = fh.read().splitlines()
    if resource in funcs:
        resource = resource.replace('-', '_')
        try:
            return True, globals()[resource]
        except KeyError:
            return False
    return False


def get_vars_from_request(varis):
    variables = varis.split('&')
    for i in range(0, len(variables)):
        variables[i] = variables[i].split('=')
    return dict(variables)


def split_resource(resource):
    resource = resource.split('?')
    method = resource[0]
    variables = get_vars_from_request(resource[1])
    return method, variables


"""
ALL BELOW ARE FUNCTIONS CALLED UPON BY A 'GET' REQUEST
DO NOT PUT ANYTHING ELSE HERE
"""


def calculate_next(variables, client_sock):
    num = int(variables['num'])
    num += 1
    result = str(num)  # result has to be string to be sent to the client correctly
    header = "HTTP/1.1 200 OK\r\n" \
             "Content-Length: {0}\r\n" \
             "\r\n".format(len(result))
    client_sock.send(header)
    client_sock.send(result)
    return header


def calculate_area(variables, client_sock):
    height = int(variables['height'])
    width = int(variables['width'])
    area = (height * width) / 2
    result = str(area)
    header = "HTTP/1.1 200 OK\r\n" \
             "Content-Length: {0}\r\n" \
             "\r\n".format(len(result))
    client_sock.send(header)
    client_sock.send(result)
    return header


def image(variables, client_sock):
    if not os.path.exists(full_running_dir + 'upload'):
        os.mkdir('upload/')
    image_name = 'upload/' + variables['image-name']
    if os.path.isfile(full_running_dir + image_name):
        with open(full_running_dir + image_name, 'rb+') as requested_resource:
            data = requested_resource.read()
            header = "HTTP/1.1 200 OK\r\n" \
                     "Content-Length: {0}\r\n" \
                     "Content-Type: {1}\r\n" \
                     "\r\n".format(len(data), get_content_type(image_name))
            client_sock.send(header)
            client_sock.sendall(data)
        return header
    bad_request(client_sock)
