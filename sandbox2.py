import csv
import re

with open('exceptions/moved_temp.csv', 'r') as fh:
    print fh.read()


with open('other/tests.txt', 'a+') as fh:
    # print fh.readline()
    # print fh.read().splitlines()
    pass

list_thing = ['hello.txt']
s = 'hello.txt'
if s in list_thing:
    pass
dit = {
    'hello': 1,
    'supp': 2,
    'dr who': 'infinity'
}


def stuff():
    with open('hello.csv', 'wb') as files_dict:
        writer = csv.writer(files_dict)
        for key, val in dit.items():
            writer.writerow([key, val])


# stuff()
"""
with open('moved_temp.csv', 'rb') as files_dict:
    reader = csv.reader(files_dict)
    new_dict = {}
    for row in reader:
        new_dict[row[0]] = row[1]

print new_dict

print "hello"
"""


def hello():
    print 'hello!'


string = "hello"
string = string.split('l')
print string

# string = raw_input()
# method = locals()[string]
# if method:
#   method()

string = 'hello!'
string = string.replace('s', 'l')
print string

if 2:
    print '2!'

with open('other/tests.txt', 'a+') as fh:
    # fh.read()
    fh.write('supp\n')


def resource_is_in_forbidden(resource, files):
    for item in files:
        search_object = re.search(item, resource)
        if search_object:
            return True


if resource_is_in_forbidden('ht.py', open('exceptions/forbidden.txt', 'r+').read().splitlines()):
    print 'HELLO'
