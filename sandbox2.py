import csv

with open('textfile.txt', 'a+') as fh:
    # print fh.readline()
    # print fh.read().splitlines()
    pass

list_thing = ['hello.txt']
s = 'hello.txt'
if s in list_thing:
    # print 'pygay'
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
# shlomo coosomo


def hello():
    print 'hello!'

string = "hellols"
string = string.split('l')
print string

string = raw_input()
method = locals()[string]
if method:
    method()