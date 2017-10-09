files =[]
for i in range(1947,2017):
    files.append(open(str(i)+'.csv','a'))
source = open('result.csv','r')
for line in source:
    year = line.replace('\n','').split(',')[1];
    files[int(year)-1947].write(line)

source.close()
for file in files:
    file.close()
print "Done!!"