with open('iplist.txt') as file:
    ipcsv = open('ip.csv','w')
    for line in file.readlines():
        for i in line:
            if i=='\n':
                ipcsv.write(',')
            else:
                ipcsv.write(i)
        