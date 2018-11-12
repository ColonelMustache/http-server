import csv

with open('textfile.txt', 'a+') as fh:
    # print fh.readline()
    # print fh.read().splitlines()
    pass

l = ['hello.txt']
s = 'hello.txt'
if s in l:
    #print 'pygay'
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

with open('moved_temp.csv', 'rb') as files_dict:
    reader = csv.reader(files_dict)
    new_dict = {}
    for row in reader:
        new_dict[row[0]] = row[1]

print new_dict

print "hello"
